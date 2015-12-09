# Fibula

This repository holds code that defines the infrastructure used to run Chiton.

## Configuration

To interact with the Chiton infrastructure, you must provide valid credentials
for the Chiton Chef organization by doing the following:

1. Add a link to the `chiton-validator.pem` file in the `.chef` directory.
2. Add a link to your personal Chef user's key in the `.chef` directory.
3. Ensure that the `CHITON_CHEF_USER_NAME` environment variable is set to the name of your personal Chef user.

Once these steps have been followed, you will be able to run Knife commands
against the Chiton organization.
