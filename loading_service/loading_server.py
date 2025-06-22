from concurrent import futures
# Importe futures pour créer un pool de threads (parallélisme léger)

import grpc
# Importe gRPC pour la communication inter-services

import sys, os
# Pour gérer les chemins de fichiers et accéder aux modules externes

# Ajoute le répertoire contenant les fichiers protobuf générés au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_interfaces', 'generated')))

# Importe les fichiers gRPC générés à partir des .proto
import loading_pb2
import loading_pb2_grpc
import common_pb2

# Importe la logique métier de chargement (non détaillée ici)
import loading_logic

# Implémentation du service LoadingService défini dans loading.proto
class LoadingServiceServicer(loading_pb2_grpc.LoadingServiceServicer):
    def LoadAll(self, request, context):
        """
        Implémentation de la méthode RPC LoadAll.
        Elle reçoit une liste de tables à charger (format TableData).
        """
        # Transforme la liste des tables en un dictionnaire {nom_table: données_bytes}
        incoming_data = {table.table_name: table.data for table in request.tables}

        # Appelle la logique métier pour charger les données
        loading_logic.load_all_data(incoming_data)

        # Renvoie une réponse de confirmation
        return common_pb2.LoadResponse(message="Data loaded successfully.")

# Fonction pour démarrer le serveur gRPC
def serve():
    # Crée un serveur gRPC avec un pool de 10 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Enregistre le service de chargement auprès du serveur
    loading_pb2_grpc.add_LoadingServiceServicer_to_server(LoadingServiceServicer(), server)

    # Écoute sur le port 50053, sur toutes les interfaces (IPv4 et IPv6)
    server.add_insecure_port('[::]:50053')

    # Affiche un message de démarrage
    print("Loading gRPC Server started at port 50053...")

    # Démarre le serveur
    server.start()

    # Attend indéfiniment la fin du serveur (exécution continue)
    server.wait_for_termination()

# Point d'entrée du fichier
if __name__ == '__main__':
    serve()
