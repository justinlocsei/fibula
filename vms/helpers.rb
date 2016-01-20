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

end
