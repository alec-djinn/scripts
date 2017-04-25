#! /usr/bin/perl

use strict;
use StrucVarDB::StrucVarDB;

my $strucVarDB = new StrucVarDB;

my $categories = $strucVarDB->getAllCategories();

foreach my $cat (@$categories) {
  my $cat_name = $cat->name();
  next unless $cat_name =~ /Reference/i;
  my $samples = $cat->getSamples();
  foreach my $sample (@$samples) {
    my $sample_name = $sample->name();
    open OUT, ">$sample_name\_$cat_name.txt";
    my $breakpoints = $sample->getBreakpoints();
    foreach my $b (@$breakpoints) {
      print OUT join("\t", $b->chr1(), $b->s1(), $b->e1(), $b->chr2(), $b->s2(), $b->e2(), $b->orientation, $b->count, $b->rProbability, $b->overlap, $b->eDistance, $b->breakType()->name) . "\n";
    }
    close OUT;
  }
}
