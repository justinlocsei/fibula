module Helpers

  # Return the absolute path to an Ansible playbook
  #
  # @param [String] name The name of the playbook
  # @return [String]
  def self.ansible_playbook(name)
    File.expand_path("../../ansible/#{name}.yml")
  end

end
