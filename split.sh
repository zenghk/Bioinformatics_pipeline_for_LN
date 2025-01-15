zcat *R1*.gz|split -a 3 -d -l 800000 && zcat *R2*.gz |split -a 4 -d -l 800000
