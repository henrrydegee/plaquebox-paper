#!/bin/bash 
# Ensure that you have installed docker and the latest nvidia graphics driver on host!
# docker outdated, use docker --gpu instead

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
IMGNAME="plaquebox"
IMGTAG="inference"
CONTNAME="infer-plaquebox"
DOCKERFILEPATH="./docker/Dockerfile"
FOLDERDIR="/home/hgunawan"
REPONAME="plaquebox-paper"
JUPYTERPORT="3366"
cd "$SCRIPTPATH"

test_retval() {
  if [ $? -ne 0 ] ; then
    echo -e "\nFailed to ${*}... Exiting...\n"
    exit 1
  fi
}

USAGE="Usage: ./setup.sh [rmimcont=[0,1]] [rmimg=[0,1]]\n"
USAGE+="\trmimcont=[0,1] : 0 to not remove intermediate Docker containers\n"
USAGE+="\t                 after a successful build and 1 otherwise\n"
USAGE+="\t                 default is 1\n"
USAGE+="\trmimg=[0,1]    : 0 to not remove previously built Docker image\n"
USAGE+="\t                 and 1 otherwise\n"
USAGE+="\t                 default is 0\n"

REMOVEIMDDOCKERCONTAINERCMD="--rm=true"
REMOVEPREVDOCKERIMAGE=false

# Parsing argument
if [ $# -ne 0 ] ; then
        while [ ! -z $1 ] ; do
                if [ "$1" = "rmimcont=0" ] ; then
                        REMOVEIMDDOCKERCONTAINERCMD="--rm=false"
                elif [ "$1" = "rmimg=1" ] ; then
                        REMOVEPREVDOCKERIMAGE=true
                elif [[ "$1" != "rmimcont=1" && "$1" != "rmimg=0" ]] ; then
                        echo -e "Unknown argument: " $1
                        echo -e "$USAGE"
                        exit 1
                fi
                shift
        done
fi

# Echo the set up information
echo -e "\n\n"
echo -e "################################################################################\n"
echo -e "\tSet Up Information\n"
if [ "$REMOVEIMDDOCKERCONTAINERCMD" = "--rm=true" ] ; then
        echo -e "\t\tRemove intermediate Docker containers after a successful build\n"
else
        echo -e "\t\tKeep intermediate Docker containers after a successful build\n"
fi
if [ "$REMOVEPREVDOCKERIMAGE" = true ] ; then
        echo -e "\t\tCautious!! Remove previously built Docker image\n"
else
        echo -e "\t\tKeep previously built Docker image\n"
fi
echo -e "################################################################################\n"

# Print usage
echo -e "\n$USAGE\n"

# Get user info
echo -e "Please identify yourself.\n\t0 - Henrry, 1 - Jeff"
read user
if [ "$user" = "0" ] ; then
	CONTNAME+="-henrry"
	JUPYTERPORT="3366"
	echo -e "Welcome, Henrry. Please use port 3366.\n"
elif [ "$user" = "1" ] ; then
	CONTNAME+="-jeff"
	JUPYTERPORT="9001"
	echo -e "Welcome, Jeff. Please use port 9001.\n"
else
	echo -e "Wrong input... Exiting...\n"
	exit 1
fi

echo -e ".......... Set up will start in 5 seconds .........."
sleep 5

# Remove previously built Docker image
if [ "$REMOVEPREVDOCKERIMAGE" = true ] ; then
        echo -e "\nRemoving previously built image..."
        docker rmi -f $IMGNAME
fi

# Build and run the image
echo -e "\nBuilding image $IMGNAME:$IMGTAG..."
docker build $REMOVEIMDDOCKERCONTAINERCMD -f $DOCKERFILEPATH -t $IMGNAME:$IMGTAG .
test_retval "build Docker image $IMGNAME:$IMGTAG"

# Build a container from the image
echo -e "\nRemoving older container $CONTNAME..."
if [ 1 -eq $(docker container ls -a | grep "$CONTNAME$" | wc -l) ] ; then
	docker rm -f $CONTNAME
fi

# Directories for Main Pipeline.ipynb
if [ ! -d "$FOLDERDIR/$REPONAME/data/wsi" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/wsi;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/norm_tiles" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/norm_tiles;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/outputs" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/outputs;
    mkdir $FOLDERDIR/$REPONAME/data/CNNscore;
    mkdir $FOLDERDIR/$REPONAME/data/outputs/heatmaps;
    mkdir $FOLDERDIR/$REPONAME/data/outputs/masked_plaque;
    mkdir $FOLDERDIR/$REPONAME/data/outputs/masked_plaque/images;
    mkdir $FOLDERDIR/$REPONAME/data/outputs/masked_plaque/numpy;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/outputs/heatmaps" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/outputs/heatmaps;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/outputs/masked_plaque" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/outputs/masked_plaque;
    mkdir $FOLDERDIR/$REPONAME/data/outputs/masked_plaque/images;
    mkdir $FOLDERDIR/$REPONAME/data/outputs/masked_plaque/numpy;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/brainseg" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/brainseg;
    mkdir $FOLDERDIR/$REPONAME/data/brainseg/images;
    mkdir $FOLDERDIR/$REPONAME/data/brainseg/numpy;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/brainseg/images" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/brainseg/images;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/brainseg/numpy" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/brainseg/numpy;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/postprocess" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/postprocess;
    mkdir $FOLDERDIR/$REPONAME/data/postprocess/images;
    mkdir $FOLDERDIR/$REPONAME/data/postprocess/numpy;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/postprocess/images" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/postprocess/images;
fi

if [ ! -d "$FOLDERDIR/$REPONAME/data/postprocess/numpy" ]; then
    mkdir $FOLDERDIR/$REPONAME/data/postprocess/numpy;
fi

# Create Docker Container
echo -e "\nBuilding a container $CONTNAME from the image $IMGNAME:$IMGTAG..."
docker create -it --name=$CONTNAME --gpus=all \
	-v "$SCRIPTPATH":/root/$REPONAME \
	-v "$FOLDERDIR/$REPONAME/data/wsi":"/root/$REPONAME/data/wsi" \
	-v "$FOLDERDIR/$REPONAME/data/norm_tiles":"/root/$REPONAME/data/norm_tiles" \
        -v "$FOLDERDIR/$REPONAME/data/outputs":"/root/$REPONAME/data/outputs" \
	-v "$FOLDERDIR/$REPONAME/data/brainseg":"/root/$REPONAME/data/brainseg" \
        -v "$FOLDERDIR/$REPONAME/data/postprocess":"/root/$REPONAME/data/postprocess" \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-e DISPLAY=$DISPLAY \
	--ipc=host \
	-p $JUPYTERPORT:$JUPYTERPORT \
	$IMGNAME:$IMGTAG /bin/bash
test_retval "create Docker container"

# Echo command to run the application
COMMANDTORUN="cd /root/$REPONAME && jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --port=$JUPYTERPORT &"
echo -e "\n\n"
echo -e "################################################################################\n"
echo -e "\tCommand to enter repository:\n\t\t${COMMANDTORUN}\n"
echo -e "################################################################################\n"

docker start -ai $CONTNAME

if [ 0 -eq $(docker container ls -a | grep "$CONTNAME$" | wc -l) ] ; then
        echo -e "\nFailed to start/attach Docker container... Exiting...\n"
        exit 1
fi

# Echo command to start container
COMMANDTOSTARTCONTAINER="docker start -ai $CONTNAME"
echo -e "\n\n"
echo -e "################################################################################\n"
echo -e "\tCommand to start Docker container:\n\t\t${COMMANDTOSTARTCONTAINER}\n"
echo -e "################################################################################\n"

