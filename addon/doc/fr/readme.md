# Weather Plus #

* Auteur : Adriano Barbieri
* Compatibilité NVDA: 2017.3 à 2019.1
* Télécharger : [version stable][1]

# A PROPOS DE WEATHER PLUS : #

* Cette extension ajoute la température locale et les prévisions météo à 24 heures actuelles et les prévisions jusqu'à 9 jours supplémentaires à NVDA.
* Copyright (C) [Adriano Barbieri](mailto:adrianobarb@yahoo.it)
* Publié sous la GNU GPL (General Public License) v2
* Version : 6.0.

# Weather Plus fonctionne à travers de l'utilisation et la présence des services suivants : #
* [https://developer.yahoo.com/weather/](https://developer.yahoo.com/weather/)
* [http://woeid.rosselliot.co.nz/lookup/](http://woeid.rosselliot.co.nz/lookup/)
* [http://www.geonames.org/](http://www.geonames.org/)
* [http://veloroutes.org/elevation/](http://veloroutes.org/elevation/)
* [https://www.timeanddate.com/](https://www.timeanddate.com/)
* [http://www.nvda.it/](http://www.nvda.it/)

# UTILISATION : #
* Appuyez sur NVDA + w pour la température actuelle et les conditions météo.
* Appuyez sur NVDA + maj + W pour les prévisions à 24 heures et les prévisions à 9 jours.
* Appuyez sur NVDA + maj + contrôle + w pour définir une ville temporaire.
* Appuyez sur NVDA + maj + contrôle + alt + w pour ouvrir la boîte de dialogue Paramètres Weather Plus.
* Appuyez sur NVDA + alt + w pour connaître la dernière mise à jour du bulletin météo.
* Appuyez sur Contrôle + maj + w pour basculer entre Fahrenheit, Celsius ou Kelvin.

# Pour configurer Weather Plus : #
Lire la section : Weather Plus Premiers Réglages.

--------------------------------------------------------------------------------

# Weather Plus Premiers Réglages : #

Vous devez  au préalable configurer l'extension Weather Plus avant sa première utilisation!

Aller dans :

Paramètres Weather Plus sous-menu

Afficher les éléments de configuration.

# Appuyer sur l'élément pour : #

* Définir et Gérer Vos Villes...
	* Affiche ou permet de définir les villes actuelles depuis une liste
* Documentation
	* Ouvre le fichier d'aide pour la langue en cours.
* Rechercher une Mise à jour...
	* Notifier si une mise à jour est disponible.

Appuyer sur l'élément :

# Définir et Gérer Vos Villes... #

Affiche ou permet de définir les villes actuelles depuis une liste

Le message suivant  s'affiche uniquement la première fois!

Paramètres Prédéfini

Aucun

F1: aide à la localisation, F2: dernière sélection avec TAB, F3: liste et zone d'édition, F4: contrôle de la durée des Prévisions Météo, F5: contrôles du volume.

Saisissez une Ville, un woeId ou sélectionnez-en une dans une liste, si disponible.

Remarque : La touche F5 est disponible si les effets sonores sont activés.

Une fois l'élément "Définir et Gérer Vos Villes..." activé, vous trouvez les boutons suivants:

# Tester #

Teste la validité du woeID de la ville saisie et cherche le nom de la ville assigné, ou vice versa.

# Ajouter #

Ajoute la ville actuelle à votre liste.

Ce bouton est activé si vous sélectionnez une ville dans la liste, et qu'elle a passée le test.

# Détails: #

Affiche des informations sur la ville actuelle.

Ce bouton est activé si vous sélectionnez une ville dans la liste, et qu'elle a passée le test.

# Définir #

Permet de définir la région, afin d'adapter les effets sonores.

Ce bouton est activé si les effets audio sont installés et activés, et vous sélectionnez une ville dans la liste.

# Prédéfini #

Définit la ville actuelle par défaut, elle sera donc utilisée chaque fois que vous redémarrerez l'extension.

Ce bouton est activé si vous sélectionnez une ville précédemment introduite dans la liste, queelle est non prédéfinie et qu'elle a passée le test.

# Supprimer #

Supprimer la ville actuelle de votre liste.

Ce bouton est activé si vous sélectionnez une ville précédemment introduite dans la liste.

# Renommer #

Renommer la ville actuelle.

Ce bouton est activé si vous sélectionnez une ville précédemment introduite dans la liste.

# Importer des nouvelles villes... #

Permet d'intégrer dans votre liste de nouvelles villes importées d'une autre liste avec l'extension *.zipcodes ; vous pouvez choisir la ville que vous souhaitez importer, en activant la case à cocher associée.

# Exporter vos villes... #

Permet d'enregistrer votre liste des villes dans un chemin d'accès spécifié.

Ce bouton est activé si vous avez ajouté et enregistré au moins une ville dans la liste.

# Échelle de mesure de la température : #

Utiliser les boutons radio pour choisire entre:

* Celsius (par défaut)
* Fahrenheit)
* Kelvin

# Indiqué les degrés comme: #

Utiliser les boutons radio pour choisire entre:

* Celsius `-` Fahrenheit `-` Kelvin (par défaut)
* C `-` F `-` K
* Non spécifié

Zone de liste déroulante :

# Prévisions Météo jusqu'à jours: 3 #

Choisissez une valeur comprise entre 1 et 10 (3 jours par défaut)

Activer/Désactiver les cases à cocher pour:

# Copier le Bulletin météo et les prévisions météo, ainsi que les détails de la ville dans le presse-papiers #

case à cocher non cochée (par défaut)

# Activer les effets audio (uniquement pour les conditions météo actuelles) #

Cette case à cocher vous permet également de gérer l'installation des effets audio;

Si les effets audio sont installés et que la case à cocher est activée, la touche F5 et le paramètre du volume deviennent disponible.

Une case à cocher supplémentaire sera également disponible:

* Utiliser uniquement des effets météo.

Vous pouvez changer le volume général ou changer le dernier effet audio entendu et filtrer les autres effets audio dans votre environnement.

case à cocher non cochée (par défaut)

# Utiliser uniquement des effets météo #

Est disponible si les effets audio sont activés;;

Si est activé, permet d'écouter uniquement les effets météo tels que la pluie, le vent, le tonnerre, etc., en filtrant tous les effets environnementaux.

case à cocher non cochée (par défaut)

# Activer la lecture des heures au format 24-heures #

Si désactivé l'heure est annoncée au format 12-heures, exemple: 12 AM `-` 12 PM.

case à cocher cochée (par défaut)

# Indiquer l'attente avec un bip pendant la recherche du dernier bulletin #

Si activée, vous entendez un bip pour indiquer l'état des recherches en cours jusqu'à ce que le dernier bulletin météo mis à jour soit trouvé.

case à cocher cochée (par défaut)

# Activez le bouton aide dans la fenêtre de paramètres #

case à cocher cochée (par défaut)

# Lire les informations du vent #

case à cocher non cochée (par défaut)

Si activé, vous pouvez également activer:

* Ajouter la direction du vent;

Indique la provenance du vent.

case à cocher cochée (par défaut)

* Ajouter la vitesse du vent;

Indique la vitesse en kilomètres ou milles par heure.

case à cocher cochée (par défaut)

* Ajouter la vitesse du vent en mètres par seconde;

case à cocher cochée (par défaut)

* Ajouter la température ressentie;

case à cocher cochée (par défaut)

# Lire les informations atmosphériques #

case à cocher non cochée (par défaut)

Si activé, vous pouvez également activer:

Ajouter le taux d'humidité;

Indique l'humidité en pourcentage.

case à cocher cochée (par défaut)

* Ajouter la valeur de visibilité;

Indique en kilomètres ou milles la distance visible.

case à cocher cochée (par défaut)

* Ajouter la valeur de la pression atmosphérique;

Indique la pression atmosphérique en millibars  ou pouces de mercure.

Si elle est cochée, active une case à cocher supplémentaire qui vous permet d'indiquer la pression en millimètres de mercure.

case à cocher cochée (par défaut)

* Ajouter l'état de la pression barométrique;

case à cocher cochée (par défaut)

# Lire les informations astronomiques #

Indique l'heure du lever et du coucher du soleil.

case à cocher non cochée (par défaut)

# Utiliser la virgule pour séparer les décimales #

Si activée, utiliser la virgule comme séparateur décimal, sinon utiliser le point.

case à cocher non cochée (par défaut)

# Rechercher une Mise à jour #

Si activée, vous recevrez une alerte lorsqu’une mise à jour de l'extension est disponible.

case à cocher cochée (par défaut)

# Appuyer sur le bouton OK pour confirmer l'action ou sur le bouton Annuler pour annuler l'action. #

Si vous avez modifié la liste des villes, en appuyant sur "Annuler", vous serez rappelé et vous pouvez toujours l'enregistrer.

# Remarque : vos réglages seront sauvegardés dans le fichier nommé: #

* "Weather.ini": paramètres de démarrage de Weather Plus.
* "Weather.volumes": niveaux de volume audio personnalisé, quel que soit le volume général.
* "Weather.zipcodes": Liste des villes avec leurs codes postaux et définitions respectifs.

--------------------------------------------------------------------------------

# Quoi de neuf : #

# Version 6.0 #
* Weather Plus revient à utiliser l'API Yahoo Weather.
* Pratiquement toutes les fonctionnalités de la version précédente 4.8 sont de retour et conserve le bouton "Renommer".
* Maintenant compatible aussi avec Python 3.

# Version 5.0.1 #
* Correction d'un bug qui renvoyait une chaîne vide si la vitesse du vent en mph était de 0.
* Correction du bug qui reproduisait les effets sonores incompatibles avec le fuseau horaire.
* Ajustement du nombre de jours de prévision de 9 à 6 dans le readme.

# Version 5.0 #
* Weather Plus utilise maintenant l'API APIXU, à mon avis mieux que la précédente.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Supprimée l'ancienne case à cocher "État de la pression barométrique".
* Remplacé par la nouvelle case à cocher "Ajouter la valeur de nébulosité";
	* Cela vous donne le pourcentage de nébulosité.
* Ajout d'une nouvelle case à cocher "Ajouter la valeur de précipitation";
	* Il vous donne la quantité de précipitation en millimètres.
* Supprimée l'ancienne case à cocher "Indiquer l'attente avec un bip pendant la recherche du dernier bulletin";
	* Il est laissé actif par défaut.
* Ajouté à les informations astronomiques;
	* Heure du lever et du coucher de la lune.
* Ajout d'un nouveau bouton "Renommer";
	* Pour renommer les villes plus facilement.
* Amélioration de la fonction du bouton "Tester";
	* Maintenant acceptent certaines commandes pour faciliter la recherche de villes;
	* Ces nouvelles commandes sont décrites dans la fonction aide pouvant être invoquée avec F1.

# Version 4.8 #
`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Ajout d'une nouvelle case à cocher;
	* "Utiliser uniquement des effets météo";
  	* Cela vous permet de filtrer tous les autres effets environnementaux.
* Amélioration de la lecture aléatoire et ajout de 71 nouveaux effets audio;
  	* Vous devrez les mettre à jour en cliquant deux fois sur la case à cocher "Activer les effets audio".
* Le type de volume attribué par l'utilisateur, entre le Volume audio général et le Volume audio actuel est maintenant conservé lors de l'enregistrement de la configuration.
* Suppression de l'effet audio inutil lors de la sélection du texte dans la zone d'édition en appuyant sur Ctrl+a.
* Amélioration de la lisibilité dans la fenêtre d’aide invocable avec la touche de fonction F1.
* Ajout d'un nouvel indicateur de compatibilité pour NVDA 2019.1 et les versions de test Alpha actuelles.

# Version 4.7.7 #
* Suppression de la notification inutile de téléchargement terminé lors de la mise à jour de Weather Plus.
* Ajout de 6 nouveaux effets audio;
	* Il sera nécessaire de les mettre à jour depuis les paramètres de l'extension.

# Version 4.7.6 #
* Correction d'un bug mineur dans la fonction GetCoords();
	* 2 valeurs n'ont pas été retournées en l'absence de connexion.

# Version 4.7.5 #
* MenuItemGetLabel() est déconseillé et a été modifiée par MenuItem.GetItemLabelText().
* Correction de certaines déclarations de variables globales.

# Version 4.7.3 #
* Mise à jour de la fonction dans "détails";
	* Pour plus de commodité, les informations sur l'altitude sont maintenant fournies par veloroutes.org.
	* Cela conduit à de petites différences de peu de pertinence.

# Version 4.7.2 #
* Correction d'un bug d'encodage dans la fonction Removeupdate.

# Version 4.7.1 #
* Correction d'un bug dans GetTimezone;
	* Dans le cas de données nulles, une valeur a été renvoyée non pas trois comme requis.

# Version 4.7 #
* Simplifié la section de mise à jour;
	* Maintenant au démarrage, dans le cas où une mise à jour est disponible, il sera possible de passer directement par une seule boîte de dialogue.
* Supprimé le sélecteur de fichier dans la section de mise à jour;
	* Maintenant, le fichier de mise à jour est téléchargé dans le dossier temporaire, ce qui permet de résoudre les problèmes dus aux utilisateurs non experts.

# Version 4.6.9 #
* Ajout de la localisation en Arabe (grâce à Wafik Immaculate).

# Version 4.6.8 #
* Mises à jour des localisations en Portugais du Portugal et en Portugais du Brésil (merci à Alberto Mendonça).

# Version 4.6.7 #
* Amélioration de la lecture de l'heure actuelle;
	* Dans certaines villes, ce n'était pas correct.
* Ajout de l'heure d'été aux détails;
	* Disponible uniquement pour les pays qui l'adoptent.

# Version 4.6.5 #
* Correction d'un petit bug lors de la lecture de l'heure actuelle;
	* Le séparateur ":" n'est pas supprimé au cours de la conversion en nombre entier.

# Version 4.6.4 #
* Amélioration de la lecture de l'heure locale actuelle; les critères de recherche sont plus précis.

# Version 4.6.2 #
* Correction d'un bug : après avoir vérifié les mises à jour, le menu "Définir une ville temporaire..." était activé même s'il n'y avait pas de liste de villes disponibles.
* Correction d'un bug : impossible de configurer WP lorsque le fichier weather.ini n'a pas encore été créé.

# Version 4.6 #
* Ajout de l'élément dans le menu  "Définir une ville temporaire...";
	* Par souci d'exhaustivité, vous pouvez maintenant ouvrir la liste de la ville temporaire à partir du menu.
* Amélioration de la gestion de l'échelle de la température;
	* Maintenant, la fenêtre des paramètres retournera toujours la valeur par défaut.
* Améliorer la prévention des multiples ouvertures des fenêtres principale;
	* Si l'une d'eux est déjà ouverte, en plus de l'alerte audio, elle se met au premier plan.
* Amélioration des effets audio;
	* Maintenant, sont basé sur l'heure locale actuelle à partir de la ville utilisée.

`#`Changements dans la fonction du bouton Détails dans la fenêtre des Paramètres:

* Ajout de l'heure locale actuelle.
* Corrigée la valeur d'altitude;
	* Maintenant, renvoie les valeurs d'altitude lorsque la valeur est inférieure ou égale à zéro.
* Corrigée la fonction d'importation;
	* Si la ville par défaut a été supprimée, elle n'apparaît plus dans la barre de titre.

# Version 4.5.5 #
* Corrigée la localisation et la documentation en Serbe.
* Corrigée la localisation en Allemand.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Ajout d'une nouvelle case à cocher;
	* Vous pouvez activer la virgule comme séparateur décimal, sinon le séparateur sera le point.

# Version 4.5.3 #
* Corrigée 2 chaînes en la localisation en Russe et en Ukrainien.
* Corrigé le titre dans la fenêtre Rechercher une Mise à jour.
* Amélioration de l'algorithme de mise à jour;
	* Maintenant, le lien vers la mise à jour est directement lu à partir de l'URL du manifeste.

# Version 4.5 #
* Ajout du raccourci clavier NVDA+maj+contrôle+alt+w;
	* Ouvre la boîte de dialogue Paramètres Weather Plus.
* Corriger certaines chaînes en Anglais.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Ajout de 8 nouvelles cases à cocher;
	* Il est maintenant possible de personnaliser davantage la sortie:
* Direction du vent.
* Vitesse du vent.
* Température ressentie.
* Valeur d'humidité.
* Valeur de visibilité.
* Valeur de la pression atmosphérique.
* Indique la pression atmosphérique en millimètres de mercure (mmHg).
* État de la pression barométrique.

# Version 4.4.8 #
* Ajout de la traduction en Polonais (grâce à Zvonimir Staneczyć).
* Weather Plus est maintenant compatible aussi avec la future version wx 4;
	* Note : en ce moment avec wx version 4.0.0b1 msw (phoenix) génère une erreur gênante lors de l'utilisation des flèches verticales dans de nombreuses boîtes d'édition :

wxAssertionError: C++ assertion "Assert failure" failed at ..\..\src\common\evtloopcmn.cpp(110) in wxEventLoopBase::Yield(): wxYield called recursively.

# Version 4.4.1 #
* Ajouté support SSL;
	* Est utilisé uniquement si une vérification du certificat d'erreur SSL a échoué.

# Version 4.4 #
* Correction d'un bug dans la lecture de la nouvelle chaîne de la version, pendant un délai de connexion.
* Amélioration de la section de mise à jour;
	* Maintenant, la boîte de dialogue n'interfère pas avec le menu nvda
* Révisée et corrigée la localisation en Russe.
* Ajout de la traduction en Ukrainien (grâce à Alex Yeshanu).

# Version 4.3.4 #
* Révisée et corrigée la localisation en Allemand.

# Version 4.3.3 #
* Ajout de la localisation en Allemand (grâce à Karl Eick).

# Version 4.3.2 #
* Ajout de la localization en roumain (grâce à Florian Ionașcu).

# Version 4.3.1 #
* Correction d'un bug mineur dans la fonction "détails";
	* Les chaînes «latitude» et «longitude» ont été inversées par rapport à la valeur.

# Version 4.3 #
* Les liens des dossiers publics deviendront inactifs le 15 mars.
	* À cette date, le dossier Public deviendra un dossier Dropbox standard et ne sera pas utilisable par l'extension.
	* Les liens pour mettre à jour l'extension et des samples ont été mis à jour, par conséquent, à partir de maintenant, WP s'appuiera complétement sur la page italienne de NVDA.

# Version 4.2.4 #
* Correction d'un bogue mineur lorsque la connexion n'était pas active.

# Version 4.2.3 #
* Maintenant, Weather Plus est capable d'exécuter quelques tentatives de connexion avant de signaler le dysfonctionnement du WoeId en cours d'utilisation, il émet un bip à chaque tentative;
	* Ce bip, Si vous le souhaitez, peut être désactivée à l'aide d'une case à cocher dans les paramètres de Weather Plus.

# Version 4.2.2 #
* Correction d'un bug dans la traduction de l'échelle de mesure;
	* Dans certaines langues, Kelvin, Celsius et Fahrenheit n'ont pas été traduits.

# Version 4.2.1 #
* Correction de l'avis de mise à jour de Weather Plus pendant le démarrage de Windows;
	* Cela se produit lorsque vous avez appuyé sur le bouton "Utiliser les paramètres NVDA actuellement sauvegardés pour l'écran de connexion à Windows (nécessite des privilèges administrateur)" à partir des Paramètres généraux de nvda, qui copie la configuration et tous les extensions dans le dossier systemConfig, mais ils ne sont pas synchronisés avec les mises à jour ultérieures des extensions.
	* Si vous avez utilisé au moins une fois cette option, vous devrez le faire à nouveau pour la dernière fois, juste après la mise à jour de Weather Plus.

# Version 4.2 #
* Ajout de 5 nouveaux effets audio;
	* Il sera nécessaire de les mettre à jour depuis les paramètres de l'extension.
* Correction d'un bug dans la fonction d'importation;
	* La liste des villes n'a pas été triée par ordre alphabétique.
* Ajout mode d'importation dans la fonction d'importation;
	* Vous pouvez décider de remplacer complètement votre propre liste, ou simplement ajouter de nouvelles villes à celle-ci.
* Mise à jour de la lecture de la prévision météo, bulletin météo actuel;
	* Ajout de la température ressentie (wind chill).
* Ajout de nouvelles chaînes à la liste bulletin météo.

# Version 4.1 #
* Correction d’un bug dans les prévisions à 10 jours;
	* Maintenant si les estimations reçues sont en nombre inférieur à la demande de l'utilisateur, les jours manquants sont indiqués comme étant inconnu.
* Correction d'une chaîne d'aide mise en place sur la commande NVDA+Maj+W.
* Documentation révisée et actualisée.

# Version 4.0 #
* Mise à jour de certaines parties du code et remplacement de toutes les instructions eval().

# Version 3.9.7 #
* Correction d’un bug pendant le ratio des prévisions météorologiques;
	* Maintenant, les températures sont lus correctement.

# Version 3.9.6 #
* Changement de l’arrondi dans la conversion de la pression atmosphérique de millibars en pouces de mercure;
	* Maintenant, la valeur est calculée en défaut, alors qu’avant il était en excès.

# Version 3.9.5 #
* Ajout de 2 nouvelles chaînes à la liste bulletin météo.
* Correction de 2 bugs.
* Mis à jour de l'exécution des sons pour l’effet dans les conditions de vent seule;
	* Maintenant le son du vent peut varier de façon aléatoire.

# Version 3.9.4 #
* Documentation, localisations pour les langues en Allemand et en Croate éliminées;
	* Car plus supportées par leurs traducteurs respectifs.
* Correction d’un bug dans la localisation en Serbe.
* Mise à jour de la localisation en Tchèque.
* Mise à jour de la documentation et la localisation en Galicien.

# Version 3.9 #
* Nouveau changement  du service API;
	* Weather Plus utilise maintenant le nouveau Yahoo Weather API avec langage Yahoo!Query et JQuery:
	* [yahoo-weather-api-with-yahooquery](http://codesimplified.blogspot.it/2013/10/yahoo-weather-api-with-yahooquery.html)
* La clé-API n’est plus nécessaire.
* Restauration de la recherche des villes homonymes;
	* Il sera possible de choisir exactement la ville souhaitée dans la liste.
* Optimisation de la sortie des sons généraux;
	* Maintenant ils sont synchronisés avec la synthèse vocale et ils sont plus rapides.
* Amélioration du Cache pour les données hors ligne;
	* Est remis à zéro toutes les 10 minutes ou seulement en changeant la ville.
* Pression barométrique mesurée en millibars ou en pouces de mercure (si les degrés sont définient en Fahrenheit).

# Version 3.8 #
* Changement du paquet de données de l'API;
	* Du format xml au format JSON, les données sont plus précises, en particulier le fuseau horaire.
* Activation du réglage automatique de la langue;
	* Maintenant l’API envoie les données des conditions météorologiques dans la langue définie par NVDA.
* Ajout d’un cache pour le bulletin et les prévisions météorologiques;
	* Si vous n'avez pas changé la ville, l'échelle de degré ou les jours des prévisions définis, vous serez capable de lire les données pendant 10 minutes même si vous vous déconnectez d'internet.
	* Le cache est réinitialisé à chaque changement décrit ci-dessus.
	* C’est parce que les bulletins ne changent pas pendant cette durrée et c'est également afin de réduire les appels fréquents à l’API, peut-être pendant la lecture avec les effets audio.
* Amélioration de la recherche des mises à jour;
	* Maintenant une fois téléchargé, l'installation démarrera, ou dans le cas d’une version portable de NVDA le dossier où vous avez enregistré la mise à jour sera ouvert.
* Mis à jour de tous les sons de notification générale;
	* Les module "tons" ne sont plus utilisés, en revanche, de petits fichiers au format WAV sont utilisés.

# Version 3.7 #
* Ajout de la possibilité de désactiver la conversion en mètres par seconde du vent.
* Ajout de la possibilité d'utiliser les unités de mesure en livres par pouce carré.
* Correction de 2 bogues.

# Version 3.6 #
* Changement du service d'API (application programming interface);
	* Maintenant WP utilise le service offert par OpenWeatherMap.org au lieu de celui offert par Yahoo Weather.com.
* Ajout de la Classification du vent dans le bulletin actuel.
* Ajout d'un pourcentage pour la nébulosité dans le bulletin actuel.
* Adoption des unités de mesure unique de la pression en hectopascal dans le bulletin actuel.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Changement de la manière d'insérer/rechercher le zipcode/woeId de yahoo dans le numéro d'ID, identificateur de la ville;
	* Les numéros   d'ID de la ville sont semblables aux woeid, mais le woeId ne fonctionnera plus, même l'ancien zipcode.
	* Vous serez en mesure de retrouver une grande partie des villes en tapant leur nom ou une partie de celui-ci.
* Ajout: insertion/recherche par coordonnées géographiques.
* Ajout: insertion/recherche par code postal.
* Amélioration de la fonction "Détails".
* Mise en place d'une aide, la touche F1 lui est assignée.
* Grâce à la touche F4 vous pourrez définir les prévisions (de 1 à 16 jours) copiées dans le presse-papiers;
	* Attention, si vous choisissez de copier dans le presse-papiers une valeur supérieure à 10, il ne sera pas lu !
* Les contrôles audio sont désormais assignés à la touche F5.
* Ajout de l'échelle de mesure en degrés Kelvin.
* Ajout de la fonction Rechercher une Mise à jour;
	* Vous pouvez définir cela dans les paramètres ou rechercher manuellement dans le menu.
* Réassignation du bouton "Trouver votre ville..." en "Gestion de votre API Key...";
	* Vous permet de saisir ou changer la clé API.

# Version 3.5 #
* Ajout de la traduction en Croate (merci à Gordan Radić).
* Ajout d'un contrôle pour le WoeId qui n'est plus valide et le Zip Code trouvé dans le réseau;
	* On a signalé des codes qui ont cessé de fonctionner d'un jour à l'autre, maintenant, WP met en garde si l'un d'entre eux a été inséré depuis la fenêtre de recherche sur le réseau.
	* Si cela se produit avec la fonction "Trouver votre ville...", Veuillez me le signaler afin que je puisse mettre à jour le Weather_buffer et les supprimer de la liste.
* Correction d'un bug dans la fonction Rechercher le suivant et précédent; elle n'avait pas l'encodage mbcs et ne pouvait pas reconnaître les caractères accentués.
* Mise à jour de la fenêtre pour définir un code postal temporaire;
	* Ajout de la fonction "Trouver" Comme dans l'autre fenêtre de Weather Plus:
	* Contrôle+F3 = Trouver..., F3 = Trouver suivant, Maj+F3 = Trouver précédent.

# Version 3.4 #
* Ajout de la traduction en Galicien (merci à Iván Novegil).
* Ajout de la traduction en Portugais (merci à Ângelo Miguel Abrantes).
* Ajout de la traduction en Allemand (incomplet).

# Version 3.3 #
* Ajout de la mesure de la vitesse du vent en mètres par secondes.
* Modification de l'encodage en "mbcs";
	* Cela permet d'utiliser également les marques diacritiques dans les noms de ville.

# Version 3.2 #
* Mise à jour de la lecture des prévisions météo, bulletin météo actuel et lecture de la date du bulletin météo actuel;
	* Yahoo weather forecast, ddepuis un peu de temps et en quantités aléatoires, permet de passer d'un historique de -10 à -5 jours pour les prévisions météo qui doivent être insérés entre les données mises à jour que nous voulons lire;
	* Il a été ajouté un filtre qui permet de lire uniquement la dernière mise à jour des données météorologiques, et un discret bip des alertes lorsque ceci intervient;
	* Ce bip, Si vous le souhaitez, peut être désactivée à l'aide d'une case à cocher dans les paramètres de Weather Plus.
	* Évidemment, le filtrage des données parfois implique un léger retard dans la réponse, mais ceci est toujours acceptable.
* Prévisions météo étendue jusq'à 10 jours.

# Version 3.1 #
* Ajout de la traduction en Serbe (merci à l'aimable coopération de Gašić Dejan `-` Gashich Deyan).
* Correction de la commande insert+alt+w;
	* Ni la validité du code postal en cours d'utilisation  ni la validité de la connexion n'étaient vérifiées comme le font les autres commandes.
* Mise à jour de la fonction de lecture des effets audio;
	* Maintenant les MP3 sont utilisés, avec une grande économie sur l'espace de disque et de temps de téléchargement, grâce à la taille réduite des fichiers compressés.
* Ajout de 41 nouveaux effets audio;
	* Il sera nécessaire de les mettre à jour depuis les paramètres de l'extension.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Correction de l'affichage de l'aide sur les boutons;
	* Maintenant l'extension désactive / active en temps réel via la case à cocher correspondante.
* Ajout de 3 raccourcis claviers pour naviguer plus rapidement dans la fenêtre:
* F1 saute dans la liste et la zone d'édition du code postal.
* F2 renvoie à la dernière sélection réalisé avec TAB.
* F3 saute dans les contrôles du volume (si les effets audio sont installés et activés).
* Ajout d'un raccourcis clavier pour toutes les cases à cocher et les boutons;
	* Omis des deux boutons radio car ils sont présents dans la succession et le premier est accessible avec la commande contrôle+maj+w.
* Modifié: le bouton "Définir" est maintenant désactivée si les effets audio ne sont pas installés et activés.
* Ajout du Contrôles du volume;
	* Vous pouvez régler le volume général et le dernier effet audio entendue;
	* Cette option est activée si les effets audio sont installés et activés.
* Ajout de la possibilité de définir l'heure du système au format 12 heures (12:30 AM `-` 12:30 PM) , ou le système 24 heures(12:30 `-` 00:30).

# Version 3.0 #
* Ajout de la traduction en Slovaque (merci à l'aimable coopération de Vitek Jirasek).
* Ajout de la traduction en Portugais-Brésilien et en Portugais-Portugal (merci à l'aimable coopération de Adair Knaesel).
* Ajout de nouvelles chaînes  à la liste bulletin météo.
* Ajout de 171 nouveaux effets audio, il y en a désormais 213.
* Ajout de la commande insert+alt+w dans le gest, annonce la date de la dernière mise à jour du bulletin météo actuel.
* Ajout d'un scriptCategory qui permet de configurer les raccourcis claviers de Weather Plus dans les "Gestes de commandes" de NVDA.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Ajout d'un bouton radio pour définir comment il faut indiquer l'échelle de température;
	* Les différents choix sont:
* Celsius `-` Fahrenheit
* C `-` F
* Aucune indication
* Ajout du bouton "Définir";
	* Il permet de définir la zone d'une ville entre:
* Arrière-pays
* Zone maritime
* Zone de désert
* Zone arctique
* Zone de montagne
	* Le choix permettra à Weather Plus d'utiliser des effets audio plus appropriés pour chaque ville individuel;
	* Voici la raison de l'augmentation du nombre de nouveaux effets audio dans cette version de l'extension;
	* Beaucoup de nouveaux effets audio que j'ai obtenu de Tapin, que je remercie sincèrement.

# Version 2.9 #
* Ajout d'une option lors de l'importation pour sélectionner le contenu du fichier importé.
* Quatre nouveaux effets de sons ont été ajoutés
* Ajout de la traduction russe (merci à Alex Yeshanu).
* Ajout de la traduction tchèque (merci à Jirimu Holzingerovi).

# Version 2.8 #
* Correction d'un bug dans "Détails"
	* Il ouvrait la fenêtre des occurrences lorsqu'il ne pouvait pas trouver la ville.
* Correction de regexp pour la recherche de l'altitude
	* Il n'acceptait pas les paramètres d'un seul chiffre.
* Amélioration de l'analyseur de la zone d'édition
	* Il devrait retrouver plus facilement la ville.
* Connexions maintenant gérées par urllib2, Au lieu de urllib
	* Cela devrait permettre le fonctionnement de l'extension même sur un ordinateur connecté au réseau d'entreprise protégé par un proxy.
* Ajout de la fonction "Trouver"
	* Contrôle+F3 = Trouver..., F3 = Trouver suivant, Maj+F3 = Trouver précédent.

# Version 2.7 #
* Correction d'un nom incorrect d'une chaîne "Motorcycle"  en "Motorcycle00"
	* Il a demandé la mise à jour des effets audio parce qu'il ne pouvait pas trouver le fichier.
* Ajout de la possibilité de lire à propos du vent ;
	* Direction, vitesse et température du vent.
* Ajout de la possibilité de lire les informations atmosphériques ;
	* Humidité, la visibilité, la pression et l'état de la pression barométrique.
* Ajout de la possibilité de lire les informations astronomiques ;
	* Heure du lever et du coucher du soleil.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Ajout de 3 cases à cocher pour gérer les informations énumérées ci-dessus.
* Ajout du bouton "Détails" ;
	* Fournit des informations telles que le vrai nom de la ville (assigné par YahooWeather Forecast), l'état / région et la nation à laquelle il appartien ;
	* Avec les coordonnées géographiques et la hauteur au-dessus du niveau de la mer.
* Ajout de la reconnaissance des  WoeID (codes de localisation, par exemple. Bologna correspond à 711080).
* Maintenant, vous pouvez taper le nom de la ville, dans ce cas, si le cas se présente, les occurrences seront répertoriés et vous serez en mesure de choisir.

# Version 2.6 #
* Les fonctions des boutons "Ajouter" et "Supprimer" ont été optimisées dans la gestion de la liste des codes postaux;
	* Maintenant  les opérations sont beaucoup plus rapide !
* La fonction du bouton "Tester" a été optimisé, maintenant jusqu'à 13 Mots clés sont utilisés;
	* Maintenant, si il ne trouve pas le nom de la ville, c'est une véritable malchance !
* La fonction du bouton "Trouver votre ville...", maintenant trouve davantage de pays;
	* Un testeur automatique qui reprend les codes postaux qui fonctionnent, et permet un affichage rapide plus tard grâce à la création d'un petit tampon correspondant au nom du pays spécifique a été ajouté.
* Trois nouveaux effets de sons ont été ajoutés;
	* Il sera nécessaire de les mettre à jour depuis les paramètres de l'extension.

# Version 2.5 #
* Ajout d'une commande dans le  geste pour basculer temporairement l'échelle de la température de Celsius en Fahrenheit, la commande est également effective dans la fenêtre des paramètres.
* Correction d'un bug, si l'utilisateur n'appuie pas sur les boutons "Ajouter" ou "Prédéfini" il n'été pas permis de prononcer le nom de la ville, puisqu'elle ne figurait pas dans la liste.
* Ajout d'une nouvelles chaînes  à la liste bulletin météo.

`#`Changements dans la fenêtre des Paramètres Weather Plus:

* Ajout d'un bouton pour ouvrir une page web de recherche afin de vérifier dans le monde entier les Codes postaux.
* Ajout de la possibilité d'importer / exporter les Codes Postaux des amis.
* Ajout de la possibilité de copier le bulletin météo ou la prévisions météo dans le presse-papiers.
* Ajout de la possibilité d'écouter les effets audio météorologiques, l'option permet également l'installation / mise à jour des effets audio.
* Ajout d'un boutons d'aide sur la gestion du Code postal.
* Changement du mode d'affichage de la fenêtre, les menus de nvda sont débridé lorsqu'il est ouvert.

# Version 2.4.4 #
* Ajout de deux chaîne à la liste bulletin météo
* Ajout des traduction Espagnole et Française (merci à Pablo Vargas et Rémy Ruiz)

# Version 2.4.3 #
* Ajout de la prévisions météo pour les 4 prochains jours
* Ajout d'une chaîne à la liste bulletin météo
* La liste Code postal temporaire est maintenant réordonnée à chaque nouvelle insertion

# Version 2.4 #
* Correction d'un bug qui empêchait d'enregistrer et gérer correctement les noms de ville contenant des voyelles accentuées.

# Version 2.3 #
* Élimination de la boîte de dialogue pour définir l'échelle de mesure de la température, une nouvelle interface graphique qui vous permet de définir tous dans une seule fenêtre a été ajoutée.
* Maintenant vous pouvez tester/ajouter/supprimer/prédéfinir comme la valeur par défaut le Code Postal recueillies sous forme de liste.
* Modification de la boîte de dialogue pour la saisie  lorsque vous avez tapé un Code Postal, maintenant en mode temporaire il vous permet de définir  un Code Postal précédemment ajoutés à la liste dans le menu À partir du menu Préférences.
* Maintenant la documentation peut être lu en anglais si le paramètre de langue n'est pas inclus dans les documents.

# Version 2.2 #
* Correction d'un bug qui ne permettait pas d'ouvrir la documentation pour les versions définitives de NVDA

# Version 2.1 #
* Correction d'un bug qui n'a pas fermer correctement l'extension, cela a empêché la mise à jour de l'icône dans la barre d'état système.

# Version 2.0 #
* Le Menu Paramètres Weather Plus  dans le sous-menu préférences a été déplacé est l'entrée  correct  n'est plus enregistrée à la volée, il est donc temporaire.
* pour appeler la ville définie dans les préférences, appuyez sur INSERT + Ctrl + f3.

# version 1.9 #
* ajout de la fonction aide a la saisie.
* ajout d'une nouvelle fonction pour une saisie rapide de Code Postal
* ajout de la lecture / écriture pour  la configuration weather.ini, maintenant, plus besoin d'éditer le fichier source.
* Menu Weather ajouté dans la barre d'état système.
* ajout du sous-menu Code Postal dans le menu paramètres.
* ajout dans le sous-menu paramètres l'échelle  de la température (Fahrenheit ou Celsius).
* ajout du menu Documentation
* ajout de la localisation Italienne

# Précédente version 1.1 #
* mise à jour NVDA-addon
* traduction provisoire à l'intérieur de la source.

--------------------------------------------------------------------------------

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=wetp
