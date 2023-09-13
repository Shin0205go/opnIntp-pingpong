import os
import subprocess

def run_docker_compose():
    try:
        # docker-compose.ymlがあるディレクトリに移動
        os.chdir('/Users/xxx/Develop/open-interpreter-docker')

        # docker-compose upを実行
        subprocess.run(["docker-compose", "up", "-d"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error executing docker-compose: {e}")

def run_command_in_container(container_name, command):
    try:
        full_command = ["docker", "exec", container_name] + command
        subprocess.run(full_command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error executing command in container: {e}")

def send_command_to_container(container_name, command, input_data=""):
    process = subprocess.Popen(
        ["docker", "exec", "-i", container_name, *command],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = process.communicate(input=input_data.encode())
    return stdout.decode(), stderr.decode()

def converse_between_containers(container_a, container_b, initial_message, rounds=2):
    message = initial_message
    command = ["interpreter", "-y", "--fast", "--max_tokens", "500"]
    for _ in range(rounds):
        # コンテナAからコンテナBへメッセージを送信
        print('コンテナAからコンテナBへメッセージを送信')
        print('message from '+container_a+" message: "+message)
        response_b, error_b = send_command_to_container(container_b, command, message)
        print('response from '+container_b+" message: "+response_b)
        if error_b:
            print(f"Error from {container_b}: {error_b}")
            return

        # コンテナBからのレスポンスをコンテナAに送信
        print('コンテナBからのレスポンスをコンテナAに送信')
        response_a, error_a = send_command_to_container(container_a, command,response_b)
        print('response from '+container_a+" message: "+response_a)
        if error_a:
            print(f"Error from {container_a}: {error_a}")
            return

        message = response_a  # 次のラウンドのためにメッセージを更新

    print(f"Finished {rounds} rounds of conversation between {container_a} and {container_b}.")

if __name__ == "__main__":
    run_docker_compose()
    
    initial_msg = "今からあなたは、別のエージェントと会話をします。pip install --upgrade open-interpreter"
    # send_command_to_container("open-interpreter-1", command, initial_msg)
    converse_between_containers("open-interpreter-1", "open-interpreter-2", initial_msg, rounds=2)
    