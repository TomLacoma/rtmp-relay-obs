import argparse

from bdd import *
import subprocess


IN_DOMAIN = "rtmp://obs.espci.fr"
OUT_DOMAIN = "rtmp://10.0.0.1"

NGINX_CONFIG_PATH = "/usr/local/nginx/conf/nginx.conf"


#Fonctions utilisées
def retrieve_flux(flux):
    """
    Détecte si un flux out (en local) est lancé, renvoie son adresse locale si oui, None sinon
    """
    fluz =  session.query(Flux).filter_by(in_flux = flux).first()

    if not fluz:
        return None
    else:
        return fluz.out_flux


def relay_flux(flux_entrant, streamkey, desc=None):
    #Création de l'objet correspondant au stream flux_entrant
    #Exemple de flux entrant : rtmp://obs.espci.fr/annee/enseignant/live
    #Ajouter le nouveau flux en db

    assert not retrieve_flux(flux_entrant), "Erreur : flux déjà existant" #Vérification que le flux n'est pas déjà existant

    flux_sortant = flux_entrant.replace(IN_DOMAIN, OUT_DOMAIN) + f"/{streamkey}" #Changement de domaine pour passer de l'exté vers le local
    flux = Flux(in_flux=flux_entrant, out_flux=flux_sortant, infos=desc)   #Nouvel objet de type flux

    session.add(flux)
    session.commit()

    refresh_flux()

    return


def refresh_flux():
    #Rebuild le fichier config nginx

    fluz = session.query(Flux).all()

    config = "rtmp{\n"

    #Récupérer le fichier standard
    with open(NGINX_CONFIG_PATH, "r") as config_file:
        base_file = config_file.read()
        base_file = base_file[:base_file.find(config)]

    config += ("server {\n"
               "\tlisten obs.espci.fr:1935;\n"
               "\tchunk_size 4096;\n\n")

    for flux in fluz:   #on remet tous les streams en cours plus celui qui a été ajouté
        new_config = (f"\tapplication pullfrom{flux.id} {{\n"
                      "\t\t live on;\n"
                      "\t\t record off;\n"
                      f"\t\t pull {flux.in_flux} live=1;\n"
                      f"\t\t push {flux.out_flux};\n"
                      "\t\t}\n")

        config += new_config
        config += "}\n\n"

    config += "}\n"

    print("Nouveau fichier de config = \n" + config) #du log


    #Modifier le fichier de config nginx
    with open(NGINX_CONFIG_PATH, "w") as config_file:
        config_file.write(base_file + config)

    subprocess.call("sudo /usr/local/nginx/sbin/nginx -s stop", shell=True) #relance Nginx
    #subprocess.call("sudo /usr/local/nginx/sbin/nginx -s stop", shell=True)
    return

#A l'exécution
parser = argparse.ArgumentParser()
parser.add_argument("flux_entrant")
parser.add_argument("streamkey")
parser.add_argument("desc", nargs="?")
args = parser.parse_args()

relay_flux(args.flux_entrant, args.streamkey, args.desc)
