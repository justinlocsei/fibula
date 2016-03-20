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

    # Return Ansible variables for a group
    #
    # @param [String] group A known Ansible group name
    # @return [Hash]
    def ansible_group_vars(group)
      vars_file = ansible_file("group_vars/#{group}")
      vars_file = "#{vars_file}/main.yml" if File.directory?(vars_file)

      begin
        YAML.load_file(vars_file)
      rescue Errno::ENOENT
        raise "No group variables defined for #{group}"
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

    # Return the local hostname for the machine
    #
    # @param [String] subdomain The subdomain for the machine
    # @return [String]
    def hostname(subdomain)
      "development-#{subdomain}.coveryourbasics.com"
    end

    # Return the path to the private key file for the Vagrant user
    #
    # @return [String]
    def private_key_path
      ENV.fetch("CYB_VAGRANT_KEY_PRIVATE")
    end

    # Options to sync a volume on the guest with the host over NFS
    #
    # @option options [String] :group_id The ID of the owning user
    # @option options [String] :guest The path to the guest directory
    # @option options [String] :host The path to the host directory
    # @option options [String] :user_id The ID of the owning user
    # @return [Array]
    def sync_guest_nfs_dir_options(options={})
      [
        options.fetch(:host),
        options.fetch(:guest),
        {
          type: "nfs_guest",
          owner: options.fetch(:user_id),
          group: options.fetch(:group_id),
          map_uid: options.fetch(:user_id),
          map_gid: options.fetch(:group_id),
          unmount_options: ["-f"]
        }
      ]
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

    # Return VirtualBox options for optimizing network performance
    #
    # This uses the host for DNS resolution, and uses the `virtio` network
    # virtualization available on newer versions of the Linux kernel.
    #
    # @return [Array<Array>] Network optimization options
    def virtualbox_networking_optimizations
      [
        ["modifyvm", :id, "--natdnshostresolver1", "on"],
        ["modifyvm", :id, "--natdnsproxy1", "on"],
        ["modifyvm", :id, "--nictype1", "virtio"],
        ["modifyvm", :id, "--nictype2", "virtio"]
      ]
    end

  end
end
