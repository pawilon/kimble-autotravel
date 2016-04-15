set -e

URL='https://201cz8f29l.execute-api.eu-west-1.amazonaws.com/prod/generate'

if [ -z "$1" ]; then
  echo "Usage: $0 travel_request_file"
fi

REQUEST="$1"

if [ ! -f $REQUEST ]; then
  echo "The file $REQUEST doesn't exist"
  exit 1
fi

if $(echo $REQUEST | grep -iq '.yaml\|.yml'); then
  # Using ruby, as it has yaml builtin, unlike Python
  cat $REQUEST | ruby -e 'require "yaml"; require "json"; puts JSON.dump(YAML.load(STDIN.read))' | curl -H "Content-Type: application/json" -XPOST --data-binary '@-' $URL
else
  cat $REQUEST | curl -H "Content-Type: application/json" -XPOST --data-binary '@-' $URL
fi
