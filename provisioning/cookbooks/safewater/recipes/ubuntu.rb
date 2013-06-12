execute "apt-get-update-force" do
  command "sudo apt-get update"
  ignore_failure true
end.run_action(:run)
