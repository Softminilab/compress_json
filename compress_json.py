import os
import json
import argparse

def validate_json(filepath):
    """
    验证指定文件中的 JSON 数据是否有效。

    Args:
        filepath (str): JSON 文件的路径。

    Returns:
        bool: True 如果 JSON 有效，False 如果 JSON 无效。
        str:  如果 JSON 无效，则返回错误消息，否则返回 None。
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)  # Try to load the JSON to validate it
        return True, None  # JSON is valid
    except json.JSONDecodeError as e:
        return False, str(e)  # JSON is invalid, return the error message
    except FileNotFoundError:
        return False, "File not found."
    except Exception as e:
        return False, str(e) #Other error

def compress_json_files(directory):
    """
    遍历指定目录下的所有json文件，进行压缩，去除空格和换行符。

    Args:
        directory (str): 要遍历的目录。
    """
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)  # Load JSON data
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)  # Dump without spaces
                    print(f"Successfully compressed: {filepath}")


                    # 验证 JSON 文件
                    is_valid, error_message = validate_json(filepath)
                    if is_valid:
                        print(f"{filepath} is valid.")
                    else:
                        print(f"❌ {filepath} is invalid: {error_message}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in {filepath}: {e}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress JSON files in a directory.")
    parser.add_argument("directory", help="The directory to process.")
    args = parser.parse_args()

    directory_to_compress = args.directory

    if not os.path.isdir(directory_to_compress):
        print(f"Error: '{directory_to_compress}' is not a valid directory.")
    else:
        compress_json_files(directory_to_compress)


