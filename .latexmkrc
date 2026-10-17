use Cwd qw(getcwd);

$pdf_mode = 1;
$out_dir = 'build';
$ENV{'TEXMFVAR'} = getcwd() . '/build/texmf-var';
$ENV{'SOURCE_DATE_EPOCH'} = '1682973407';
$ENV{'FORCE_SOURCE_DATE'} = '1';

# The archived 2023 build used a Metafont bitmap for TS1 list bullets.
# Disable the newer installation's CM-Super substitution for this font only.
$pdflatex = 'pdflatex %O "\pdfmapline{-tcrm1095}\input{%S}"';
