require "yaml"

module Fibula
  class << self

    # Return the absolute path to an Ansible file
    #
    # @param [String] path The path to the file, relative to the Ansible root
    # @return [String]
    def ansible_file(path)
      File.expand_path("../../ansible/#{path}")
    end

    # Return the host-specific Ansible variables
    #
    # @param [String] host A known Ansible hostname
    # @return [Hash]
    def ansible_host_vars(host)
      vars_file = ansible_file("host_vars/#{host}")
      vars_file = "#{vars_file}/main.yml" if File.directory?(vars_file)

      begin
        YAML.load_file(vars_file)
      rescue Errno::ENOENT
        raise "No host variables defined for #{host}"
      end
    end

    # Configure Ansible to prompt for a vault password or use a password file
    #
    # @param [] ansible An Ansible provisioner instance
    def configure_ansible_vault(ansible)
      password_file = ENV["CYB_ANSIBLE_VAULT_PASSWORD_FILE"]

      if password_file && File.exist?(password_file)
        stats = File.stat(password_file)
        mode = sprintf("%o", stats.mode)

        if mode[-2..-1] != "00"
          raise "The Ansible vault-password file must not be group- or world-readable"
        else
          ansible.vault_password_file = password_file
        end
      else
        ansible.ask_vault_pass = true
      end
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

    # Return the path to the private key file for the Vagrant user
    #
    # @return [String]
    def private_key_path
      ENV.fetch("CYB_VAGRANT_KEY_PRIVATE")
    end

    # Options to pass to a synced folder to sync the home directory
    #
    # @param [String] path The guest path to the home directory
    # @return [Array]
    def sync_home_options(path)
      [
        File.expand_path("~"),
        path,
        {
          :rsync__auto => false,
          :rsync__exclude => "*/",
          :type => "rsync"
        }
      ]
    end

  end
end
