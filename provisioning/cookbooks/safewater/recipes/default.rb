
execute "apt-get-update-periodic" do
  command "apt-get update"
  ignore_failure true
  only_if do
    ::File.exists?('/var/lib/apt/periodic/update-success-stamp') &&
    ::File.mtime('/var/lib/apt/periodic/update-success-stamp') < Time.now - 86400
  end
end

# install packages we need for safewater athens

%w{libapache2-mod-wsgi libapache2-mod-php5 supervisor python-dev}.each do |pkg|
  package pkg
end

# set up files

directory "/opt/water" do
  owner "water"
  group "water"
  mode 0775
  action :create
end

%w{var data}.each do |dir|
  directory "/opt/water/#{dir}" do
    owner "water"
    group "water"
    mode 0775
    action :create
  end
end

# set up apache

apache_module "wsgi" do
   enable true
end

apache_module "php5" do
    filename "libphp5.so"
end

apache_site "safewater-athens" do
    enable true
end

web_app "safewater-athens" do
    server_name node['safewater']['virtual_hostname']
    server_aliases ['athens.' + node['safewater']['virtual_hostname']]
    docroot "/opt/water/app/site/"
end

# allow apparmor to allow mysql to run out of the /opt/water/data/mysql dir

cookbook_file "/etc/apparmor.d/local/usr.sbin.mysqld" do
    action :create_if_missing
    path "/etc/apparmor.d/local/usr.sbin.mysqld"
    source "apparmor.usr.sbin.mysqld"
    owner "root"
    group "root"
    mode "755"
end

# setup python env

vc_python_virtualenv "/opt/water/var" do
    owner "water"
    group "water"
    interpreter "python2.7"
    action :create
end

vc_python_pip "distribute" do
    virtualenv "/opt/water/var"
    action :upgrade
end

vc_python_pip "-" do
    virtualenv "/opt/water/var"
    requirements "/opt/water/app/requirements.txt"
    action :install
end

# set up mysql

mysql_connection_info = { :host => "localhost",
                          :usermame => "root",
                          :password => node['mysql']['server_root_password']}

mysql_database node['safewater']['mysql']['database'] do
  connection mysql_connection_info
  action :create
end

mysql_database_user node['safewater']['mysql']['user'] do
    connection mysql_connection_info
    password node['safewater']['mysql']['password']
    database_name node['safewater']['mysql']['database']
    host '%'
    privileges [:all]
    action :grant
end

# Do the syncdb

bash "syncdb" do
  user "root"
  cwd "/tmp"
  code <<-EOH
  cd /opt/water/app
  . bin/activate
  ./manage.py syncdb --migrate --noinput
  EOH
end


# Restart apache to bring up the app

bash "restart apache" do
  user "root"
  cwd "/tmp"
  code "service apache2 reload"
end



# vvvv from examples vvvv

#   celery do
#     only_if { node['roles'].include? 'safewater_app' }
#     config "celery_settings.py"
#     django true
#     celerybeat true
#     celerycam true
#     broker do
#       transport "redis"
#     end
#   end


#   gunicorn do
#     only_if { node['roles'].include? 'safewater_app' }
#     app_module :django
#     port 8080
#   end

#   django do
#     packages ["redis"]
#     # requirements "requirements/mkii.txt"
#     # settings_template "settings.py.erb"
#     debug true
#     collectstatic "build_static --noinput"
#     database do
#       database "safewater"
#       engine "mysql"
#       username "safewater"
#       password "nocrypt0"
#     end
#   end

