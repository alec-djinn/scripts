#! /usr/bin/perl

use strict;
use Data::Dumper;
use Try::Tiny;
#use lib '/data/tools/ensembl/ensembl72/modules';
#use lib '/data/tools/ensembl/ensembl72-variation/modules';
## use lib '/data/tools/ensembl/ensembl75/ensembl/modules';
## use lib '/data/tools/ensembl/ensembl75/ensembl-variation/modules';
#use lib '/data/tools/ensembl/bioperl-live';
use lib "$ENV{HOME}/src/ensembl72/modules";
use lib "$ENV{HOME}/src/ensembl72-variation/modules";
use lib "$ENV{HOME}//bioperl-live";
use Bio::EnsEMBL::Registry;

print "Modules loaded correctly\n";

my $reg = "Bio::EnsEMBL::Registry";
$reg->load_registry_from_db(-host => 'wgs10.op.umcutrecht.nl', -user => 'ensembl');
# $reg->load_registry_from_db(-host    => 'ensembldb.ensembl.org', -user    => 'anonymous');
my $sa = $reg->get_adaptor("human", "core", "slice"); 

my $file = shift;
open F, $file;
my $header = <F>;
print $header;
while(my $line = <F>) {
  chomp($line);
  my @line = split/\t/, $line;
  print $line;
  my $donor_transcript = $line[17];
  my $donor_pos = $line[4];
  $donor_pos = $line[3] if $line[5] eq "-";
  my $acceptor_transcript = $line[26];
  my $acceptor_pos = $line[7];
  $acceptor_pos = $line[8] if $line[9] eq "-";
  my $donor_domains = getDomains($donor_transcript, $donor_pos, "donor");
  print "\t" . $donor_domains;
  my $acceptor_domains = getDomains($acceptor_transcript, $acceptor_pos, "acceptor");
  print "\t" . $acceptor_domains;
  print "\n";
}

sub getDomains {
  my ($transcript_id, $pos, $type) = @_;
  try {
    my $slice = $sa->fetch_by_transcript_stable_id($transcript_id);
    my $domains;
    my $transcripts = $slice->get_all_Transcripts();
    foreach my $transcript (@$transcripts) {
      next unless $transcript->display_id() eq $transcript_id;
      my $trmapper = Bio::EnsEMBL::TranscriptMapper->new($transcript); 
      my $translation = $transcript->translation();
      my $proteinfeatures = $translation->get_all_ProteinFeatures('Pfam');
      foreach my $pf (@$proteinfeatures) {
	my @genomic = $trmapper->pep2genomic($pf->start, $pf->end);
	my ($genomic_start, $genomic_end) . "\n";
	my $flag = 0;
	if ($transcript->strand() == 1) {
	  $genomic_start = $slice->start()+$genomic[0]->start;
	  $genomic_end = $slice->start()+$genomic[-1]->end;
	  $flag = 1 if $pos <= $genomic_start and $type eq "acceptor";
	  $flag = 1 if $pos >= $genomic_end and $type eq "donor";
	} elsif ($transcript->strand() == -1) {
	  $genomic_start = ($slice->start()+$genomic[-1]->end);
	  $genomic_end = $slice->start()+$genomic[0]->start;
	  $flag = 1 if $pos >= $genomic_end and $type eq "acceptor";
	  $flag = 1 if $pos <= $genomic_start and $type eq "donor";
	}
	$domains .= $pf->idesc() . ":$genomic_start-$genomic_end;" if $flag;
      }
    }
    return($domains);
  } catch {
    return("");
  };
}