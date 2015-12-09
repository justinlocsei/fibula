current_dir = File.dirname(__FILE__)
chef_user_name = ENV["CHITON_CHEF_USER_NAME"]

log_level    :info
log_location STDOUT

chef_server_url        "https://api.chef.io/organizations/chiton"
client_key             "#{current_dir}/#{chef_user_name}.pem"
cookbook_path          ["#{current_dir}/../chef/cookbooks"]
node_name              "#{chef_user_name}"
validation_client_name "chiton-validator"
validation_key         "#{current_dir}/chiton-validator.pem"
