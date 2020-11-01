# rtmp-relay-obs
Relais RTMP vers nginx avec deux trois trucs sympas


main.py --source=rtmp://faeziuhbazoeiufhabzeoifuahn/ke
-> aller en db voir si le flux existe
-> si oui: planter, renvoyer le lien existant, return
-> si non:
    -> créer la session nginx sur passerelle
    -> créer l'entrée en db avec pid(primaire)/lien interne rez/lien externe/matire, prof, infos du cul
    -> return lien interne

www.obs.rez pour voir tous les flux

Si besoin :
main.py --kill=truc
-> tuer "truc" si existant (session nginx)

C'est une rediff ?

"""
  Template fichier config:
  rtmp {
      server {
          listen 1935;
          chunk_size 4096;

      application pullfrompublisher {
          live on;
          record off;
          pull rtmp://10.2.4.5:2935/ocpush/cnoc live=1;
          }

      application pushtotwitch {
          live on;
          record off;
          push rtmp://live.twitch.tv/live/streamkey;
          }
      }
  }
  """
