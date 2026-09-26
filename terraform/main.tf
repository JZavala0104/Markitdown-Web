# Script que se ejecuta al encender la VM por primera vez
locals {
  custom_data = <<CUSTOM_DATA
#!/bin/bash
apt-get update
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
usermod -aG docker devopsuser
CUSTOM_DATA
}

resource "azurerm_linux_virtual_machine" "vm_markitdown" {
  name                = "vm-markitdown-prod"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_B1s" # Tamaño gratuito/económico
  admin_username      = "devopsuser"
  
  # Inyectamos el script para instalar docker
  custom_data = base64encode(local.custom_data)

  admin_ssh_key {
    username   = "devopsuser"
    public_key = file("~/.ssh/id_rsa.pub") # Tu llave SSH local
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}