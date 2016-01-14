current_dir = File.dirname(__FILE__)
chef_user_name = ENV["CYB_CHEF_USER_NAME"]

log_level    :info
log_location STDOUT

chef_server_url        "https://api.chef.io/organizations/coveryourbasics"
client_key             "#{current_dir}/#{chef_user_name}.pem"
cookbook_path          ["#{current_dir}/../chef/cookbooks"]
node_name              "#{chef_user_name}"
validation_client_name "coveryourbasics-validator"
validation_key         "#{current_dir}/coveryourbasics-validator.pem"
