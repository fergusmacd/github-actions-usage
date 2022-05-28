terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "<your-org>"

    workspaces {
      name = "<change-me>"
    }
  }
}
