#!/bin/bash

sed -Ei "s/: None/: 'None'/g" stocks.pl
cat stocks.pl | tr '{' '[' | tr '}' ']' > temp.pl
mv temp.pl stocks.pl
