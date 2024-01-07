#!/bin/bash

CONNECTION_FILE="$HOME/.ssh_connections"

add_connection() {
    echo "Entrez le nom d'utilisateur :"
    read username
    echo "Entrez le mot de passe :"
    read -s password
    echo "Entrez l'hôte (adresse IP ou nom de domaine) :"
    read host
    echo "$username,$password,$host" >> $CONNECTION_FILE
}

select_connection() {
    if [ ! -f $CONNECTION_FILE ]; then
        echo "Aucune connexion disponible."
        return
    fi

    PS3='Sélectionnez la connexion à utiliser : '
    connections=$(cat $CONNECTION_FILE)
    select conn in $connections; do
        IFS=',' read username password host <<< "$conn"
        echo "Connexion à $host avec l'utilisateur $username..."
        sshpass -p $password ssh $username@$host
        break
    done
}

if [ "$1" == "--add" ]; then
    add_connection
else
    select_connection
fi
