import bdd
import subprocess

IN_DOMAIN = "rtmp://obs.espci.fr"
OUT_DOMAIN = "rtmp://10.0.0.1"

NGINX_CONFIG_PATH = "/etc.nginx/nginx.conf"

def retrieve_flux(flux):
    """
    Détecte si un flux out (en local) est lancé, renvoie son adresse locale si oui, None sinon
    """
    fluz =  session.query(Flux).filter_by(out_flux = flux).all()

    if not fluz:
        return None
    else:
        return fluz.out_flux


def relay_flux(flux_entrant, streamkey, desc=None):
    #Création de l'objet correspondant au stream flux_entrant
    #flux entrant : rtmp://obs.espci.fr/annee/enseignant/live
    #Ajouter le nouveau flux en db

    flux_sortant = flux_entrant.replace(IN_DOMAIN, OUT_DOMAIN) + streamkey #Changement de domaine pour passer de l'exté vers le local
    flux = Flux(id, flux_entrant, flux_sortant, desc)   #Nouvel objet de type flux

    session.add(flux)
    session.commit()

    #Rebuild le fichier config nginx

    fluz = session.query(Flux).all()

    config = "rtmp{\n"

    for flux in fluz:   #on remet tous les streams en cours plus celui qui a été ajouté
        new_config = ("server {\n"
                    "\tlisten 1935;\n"
                    "\tchunk_size 4096;\n"
                    f"\tapplication pullfrom{flux.id} {{\n"
                    "\t\t live on;\n"
                    "\t\t record off;\n"
                    f"\t\t pull {flux.in_flux} live=1;\n"
                    "\t\t}\n"
                    "\tapplication pushtotwitch {\n"
                    "\t\t live on;\n"
                    "\t\t record off;\n"
                    f"\t\t push {flux.out_flux};\n"
                    "\t\t}\n")

        config += new_config
    config += "}"

    print("Nouveau fichier de config = \n" + config) #du log

    #Modifier le fichier de config nginx
    with open(NGINX_CONFIG_PATH, "w") as config_file:
        config_file.write(config)

    subprocess.call("sudo systemctl restart nginx")



    return fluz

    #return un truc qui dit si ça s'est bien passé
