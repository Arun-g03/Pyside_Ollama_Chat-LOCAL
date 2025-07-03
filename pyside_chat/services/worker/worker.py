from PySide6.QtCore import QObject, Signal
import requests
import json

class Worker(QObject):
    update_message_signal = Signal(str)
    stream_chunk_signal = Signal(str)
    finished_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False

    def run(self, message):
        """
        Run the worker task.
        """
        try:
            self._running = True
            # Simulate long-running task or response fetching
            response = message
            self.update_message_signal.emit(response)
        except Exception as e:
            self.update_message_signal.emit(f"Error: {str(e)}")
        finally:
            self._running = False
            self.finished_signal.emit()

    def stop(self):
        """
        Stop the worker.
        """
        self._running = False

    def is_running(self):
        """
        Check if the worker is currently running.
        """
        return self._running

    def run_stream(
        self,
        messages,
        model,
        temperature,
        ollama_url,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty
    ):
        try:
            url = f"{ollama_url}/chat"
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "stream": True
            }
            with requests.post(url, json=data, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        #logger.debug("STREAM CHUNK:", content,print_to_terminal=True)
                        if content:
                            self.stream_chunk_signal.emit(content)
                        if chunk.get("done", False):
                            break
        except Exception as e:
            self.update_message_signal.emit(f"Error: {str(e)}")
        finally:
            self.finished_signal.emit()
