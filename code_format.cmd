@echo off

echo "--------- ISORT ---------"
isort api
echo "-------------------------"

echo "--------- BLACK ---------"
black api
echo "-------------------------"
