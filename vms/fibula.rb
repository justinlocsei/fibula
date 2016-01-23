module Fibula
  class << self

    # A hash defining network information for named VMs
    BINDINGS = {
      :himation => {
        :ip => "10.2.1.6",
        :port => 8080
      }
    }

    private_constant :BINDINGS

    # Return the absolute path to an Ansible file
    #
    # @param [String] path The path to the file, relative to the Ansible root
    # @return [String]
    def ansible_file(path)
      File.expand_path("../../ansible/#{path}")
    end

    # Return the absolute path to a VM box
    #
    # @param [String] box The name of a box
    # @return [String]
    def box_path(box)
      File.expand_path("../../packer/build/boxes/#{box}.box")
    end

    # Return the IP address for a given VM
    #
    # @param [Symbol] vm The ID of a VM
    # @return [String]
    def ip(vm)
      BINDINGS.fetch(vm).fetch(:ip)
    end

    # Return a hash of options for mounting a synced folder over NFS
    #
    # @return [Hash]
    def nfs_options
      {
        :mount_options => %w[actimeo=1 fsc tcp vers=3],
        :type => "nfs"
      }
    end

    # Return the port on which a VM listens for traffic
    #
    # @param [Symbol] vm The ID of a VM
    # @return [Number]
    def port(vm)
      BINDINGS.fetch(vm).fetch(:port)
    end

    # Return the absolute path to a project
    #
    # @param [String] name The name of the project
    # @return [String]
    def project_directory(name)
      File.expand_path("#{ENV['CYB_PROJECTS_DIR']}/#{name}")
    end

    # Return the path to the private key file for the Vagrant user
    #
    # @return [String]
    def private_key_path
      ENV["CYB_VAGRANT_KEY_PRIVATE"]
    end

  end
end
