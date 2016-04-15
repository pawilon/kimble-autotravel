set -e

# A little stack overflow copy pasta never hurt anyone, did it?
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

HANDLER=$DIR/serverless-autotravel-python/functions/generate/handler.py

if [ -z "$1" ]; then
  echo "Usage: $0 travel_request_file"
fi

REQUEST="$1"

if [ ! -f $REQUEST ]; then
  echo "The file $REQUEST doesn't exist"
  exit 1
fi

CODE="import imp; import sys; import json; handler = imp.load_source('handler', '$HANDLER'); json_file=json.loads(sys.stdin.read()); print handler.handler(json_file, {})"

if $(echo $REQUEST | grep -iq '.yaml\|.yml'); then
  # Using ruby, as it has yaml builtin, unlike Python
  cat $REQUEST | ruby -e 'require "yaml"; require "json"; puts JSON.dump(YAML.load(STDIN.read))' | python -c "$CODE"
else
  cat $REQUEST | python -c "$CODE"
fi
