module Helpers

  ADDRESSES = {
    :himation => {
      :ip => "10.1.0.0",
      :port => 8080
    }
  }

  # Return the absolute path to an Ansible file
  #
  # @param [String] path The path to the file, relative to the Ansible root
  # @return [String]
  def self.ansible_file(path)
    File.expand_path("../../ansible/#{path}")
  end

  # Return the absolute path to a project
  #
  # @param [String] name The name of the project
  # @return [String]
  def self.project_directory(name)
    File.expand_path("#{ENV['CYB_PROJECTS_DIR']}/#{name}")
  end

  # Return the path to the private key file for the Vagrant user
  #
  # @return [String]
  def self.private_key_path
    ENV["CYB_VAGRANT_KEY_PRIVATE"]
  end

end
