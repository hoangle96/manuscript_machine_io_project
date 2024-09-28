import polars as pl 
from pathlib import Path

df = pl.read_csv('papers.csv')
df['full_text']