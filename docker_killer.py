import subprocess

def get_running_containers():
    # Run 'docker ps' and capture the output
    result = subprocess.run(['docker', 'ps'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    # Extract the container IDs from the output
    lines = output.splitlines()[1:]  # Skip the header line
    container_ids = [line.split()[0] for line in lines]

    return container_ids

def get_process_id(container_id):
    # Run 'ps -ef | grep <container_id>' and capture the output
    result = subprocess.run(['ps', '-ef'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    # Find the line containing the container_id and extract the first process ID
    for line in output.splitlines():
        if container_id in line and 'grep' not in line:
            return line.split()[1]
    
    return None

def kill_process(process_id):
    # Run 'sudo kill -9 <process_id>'
    subprocess.run(['sudo', 'kill', '-9', process_id])

def restart_docker():
    # Restart the Docker service
    subprocess.run(['sudo', 'systemctl', 'restart', 'docker'])
    print("Docker service restarted.")

def prune_containers():
    # Prune unused containers
    subprocess.run(['docker', 'container', 'prune', '-f'])
    print("Unused Docker containers pruned.")

def main():
    container_ids = get_running_containers()

    for container_id in container_ids:
        process_id = get_process_id(container_id)
        if process_id:
            print(f"Killing process {process_id} for container {container_id}")
            kill_process(process_id)
        else:
            print(f"No process found for container {container_id}")

    # Restart Docker and prune containers
    restart_docker()
    prune_containers()

if __name__ == "__main__":
    main()
