module Helpers

  # Return the absolute path to an Ansible file
  #
  # @param [String] path The path to the file, relative to the Ansible root
  # @return [String]
  def self.ansible_file(path)
    File.expand_path("../../ansible/#{path}")
  end

end
