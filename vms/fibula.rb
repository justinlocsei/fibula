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

    # Return the options passed to bindfs when mounting an NFS share
    #
    # @return [Hash]
    def bindfs_options
      {
        :group => "vagrant",
        :owner => "vagrant"
      }
    end

    # Return the IP address for a given VM
    #
    # @param [Symbol] vm The ID of a VM
    # @return [String]
    def ip(vm)
      BINDINGS.fetch(vm).fetch(:ip)
    end

    # Optimize the network configuration for a VM's VirtualBox provider
    #
    # This uses the host for DNS resolution, and uses the `virtio` network
    # virtualization available on newer versions of the Linux kernel.
    #
    # @param [] vbox A VirtualBox configuration instance
    def optimize_virtualbox_networking(vbox)
      vbox.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vbox.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      vbox.customize ["modifyvm", :id, "--nictype1", "virtio"]
      vbox.customize ["modifyvm", :id, "--nictype2", "virtio"]
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
      File.expand_path("#{ENV.fetch('CYB_PROJECTS_DIR')}/#{name}")
    end

    # Return the path to the private key file for the Vagrant user
    #
    # @return [String]
    def private_key_path
      ENV.fetch("CYB_VAGRANT_KEY_PRIVATE")
    end

    # Options to pass to a synced folder to sync the home directory
    #
    # @return [Array]
    def sync_home_options
      [
        File.expand_path("~"),
        "/vagrant-user-home",
        {
          :rsync__auto => false,
          :rsync__exclude => "*/",
          :type => "rsync"
        }
      ]
    end

  end
end
