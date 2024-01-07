class Lssh < Formula
    desc "SSH Connection Manager"
    homepage "https://github.com/JamesStandbridge/homebrew-lssh"
    url "URL_DE_VOTRE_SCRIPT"
    sha256 "SHA256_DE_VOTRE_SCRIPT"
  
    def install
      bin.install "lssh.sh"
      bin.install_symlink "#{bin}/lssh.sh" => "lssh"
    end
  end
  