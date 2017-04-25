#! /usr/bin/perl

### VERSION 31_July_2015 : modified by alessio.marcozzi@gmail.com

# Set libraries:
use strict;
use Data::Dumper;
use lib "$ENV{HOME}/src/bioperl-1.2.3";
use lib "$ENV{HOME}/src/ensembl72/modules";
use lib "$ENV{HOME}/src/ensembl72-variation/modules";
# use lib '/Users/amarcozzi/src/bioperl-1.2.3';
# use lib '/Users/amarcozzi/src/ensembl72/modules';
# use lib '/Users/amarcozzi/src/ensembl72-variation/modules';
use Bio::EnsEMBL::Registry;

#print Dumper (\@INC);


# Body
my $reg = "Bio::EnsEMBL::Registry";
my $server = 'wgs10.op.umcutrecht.nl';
my $login_user = 'ensembl';

$reg->load_registry_from_db(-host => $server, -user => $login_user);

my $sa = $reg->get_adaptor("human", "core", "slice");
my $file = shift;

open F, $file;
while(my $line = <F>) {

  chomp($line);
  next if $line =~ /^#/;
  next if $line eq "";
  next if $line =~ /^REFERENCE/;
  print $line . "\n";
  my ($id, $chr1, $s1, $e1, $chr2, $s2, $e2, $type, $ori) = split/\t/, $line;
  $chr1 = "X" if $chr1 == 23;
  $chr1 = "Y" if $chr1 == 24;
  $chr2 = "X" if $chr2 == 23;
  $chr2 = "Y" if $chr2 == 24;
  my ($pos1, $pos2) = ($s1, $s2);
  if ($ori =~ /(H|T)(H|T)/i) {
    $pos1 = $e1 if $1 eq "T";
    $pos2 = $e2 if $2 eq "T";
  }
  
  my ($genes1) = getGenesOverlap($chr1, $pos1);
  my ($genes2) = getGenesOverlap($chr2, $pos2);
  
  my ($fusions) = getFusions($genes1, $genes2, $pos1, $pos2, $ori);
  foreach my $fusion (@$fusions) {
#     print join("\t", $id, $chr1, $s1, $e1, $chr2, $s2, $e2, $type, $ori) . "\t" . $fusion . "\n";
    print $line . "\t" . $fusion . "\n";
  }
  
}
close F;


# Functions
sub getGenesOverlap {
  my ($chr, $pos) = @_;
  my $slice = $sa->fetch_by_region('chromosome', $chr, $pos, $pos);
  my $allGenes = $slice->get_all_Genes();
  my %genes;
  foreach my $gene (@{$allGenes}) {
    next unless $gene->biotype eq "protein_coding";
    my $strand = "+";
    $strand = "-" if $gene->strand() == -1;
    my $name = $gene->external_name;
    $genes{$name}{'strand'} = $strand;
    $genes{$name}{'id'} = $gene->display_id;
    my $transcripts = $gene->get_all_Transcripts();
    my $length = 0;
    my $transId;
    my $exons;
    foreach my $trans (@$transcripts) {
      next unless $trans->biotype eq "protein_coding";
      next unless $trans->length > $length;
      $transId = $trans->display_id;
      $exons = $trans->get_all_Exons();
      $length = $trans->length;      
    }       
    next unless $exons;
    $genes{$name}{'transcript'} = $transId;
    $genes{$name}{'total_exons'} = scalar(@$exons);
    foreach my $exon (@$exons) {
      $genes{$name}{'exons'}{$exon->display_id}{'start_phase'} = $exon->phase;
      $genes{$name}{'exons'}{$exon->display_id}{'end_phase'} = $exon->end_phase;
      if ($strand eq "+") {
	$genes{$name}{'exons'}{$exon->display_id}{'seq_region_start'} = $exon->seq_region_start;
	$genes{$name}{'exons'}{$exon->display_id}{'seq_region_end'} = $exon->seq_region_end;      
      } else {
	$genes{$name}{'exons'}{$exon->display_id}{'seq_region_start'} = $exon->seq_region_end;
	$genes{$name}{'exons'}{$exon->display_id}{'seq_region_end'} = $exon->seq_region_start;
      }
    }
  }
  return(\%genes);
}


sub getFusions {
  my ($genes1, $genes2, $pos1, $pos2, $ori) = @_;
  my $fusion = "Not in Frame";
  my $phase = "Not in Phase";
  my ($o1, $o2);
  if ($ori =~ /^(H|T)(H|T)/i) {
    $o1 = uc($1);
    $o2 = uc($2);
  }
  my $rank1 = 1;
  my $exonNumber1 = 0;
  my $phase1 = -2;   
  my $rank2 = 1;
  my $exonNumber2 = 0;
  my $phase2 = -2;
  
  
  my @fusions;
    
  foreach my $gene1 (keys %{$genes1}) {
    my $str1 = $genes1->{$gene1}{strand};
    my @exons1 = sort{$genes1->{$gene1}{'exons'}{$a}{'seq_region_start'} <=> $genes1->{$gene1}{'exons'}{$b}{'seq_region_start'} } keys %{$genes1->{$gene1}{'exons'}} if $str1 eq "+";
    @exons1 = sort{$genes1->{$gene1}{'exons'}{$b}{'seq_region_start'} <=> $genes1->{$gene1}{'exons'}{$a}{'seq_region_start'} } keys %{$genes1->{$gene1}{'exons'}} if $str1 eq "-";   
     foreach my $exon (@exons1) {
      my $exonStart = $genes1->{$gene1}{'exons'}{$exon}{'seq_region_start'};
      my $exonEnd = $genes1->{$gene1}{'exons'}{$exon}{'seq_region_end'};
      if ($str1 eq "+") {
	if ($o1 eq "H") {
	  if ($pos1 >= $exonStart and $pos1 <= $exonEnd) {
	    $exonNumber1 = $rank1;
	    $phase1 = "exonic";
	    $phase1 .= "(". ($genes1->{$gene1}{'exons'}{$exon}{'start_phase'}+(abs($pos1-$exonStart))) % 3 . ")";
	  } elsif ($pos1 < $exonStart) {
	    $phase1 = $genes1->{$gene1}{'exons'}{$exon}{'start_phase'};
	    $exonNumber1 = $rank1;
	    last;
	  }
	} elsif ($o1 eq "T") {
	  if ($pos1 >= $exonStart and $pos1 <= $exonEnd) {
	    $exonNumber1 = $rank1;
	    $phase1 = "exonic";
	    $phase1 .= "(". ($genes1->{$gene1}{'exons'}{$exon}{'start_phase'}+(abs($pos1-$exonStart))) % 3 . ")";
	  } elsif ($pos1 > $exonEnd) {
	    $phase1 = $genes1->{$gene1}{'exons'}{$exon}{'end_phase'};
	    $exonNumber1 = $rank1;
	  }
	}
      }
      elsif ($str1 eq "-") {
	if ($o1 eq "H") {
	  if ($pos1 <= $exonStart and $pos1 >= $exonEnd) {
	    $exonNumber1 = $rank1;
	    $phase1 = "exonic";
	    $phase1 .= "(". ($genes1->{$gene1}{'exons'}{$exon}{'start_phase'}+(abs($pos1-$exonStart))) % 3 . ")";
	  } elsif ($pos1 < $exonEnd) {
	    $phase1 = $genes1->{$gene1}{'exons'}{$exon}{'end_phase'};
	    $exonNumber1 = $rank1;
	  }
	} elsif ($o1 eq "T") {
	  if ($pos1 <= $exonStart and $pos1 >= $exonEnd) {
	    $exonNumber1 = $rank1;
	    $phase1 = "exonic";
	    $phase1 .= "(". ($genes1->{$gene1}{'exons'}{$exon}{'start_phase'}+(abs($pos1-$exonStart))) % 3 . ")";
	  } elsif ($pos1 > $exonStart) {
	    $phase1 = $genes1->{$gene1}{'exons'}{$exon}{'start_phase'};
	    $exonNumber1 = $rank1;
	  }
	}
      }
      $rank1++;
    }
    if (scalar(keys %{$genes2} == 0)) {
      push @fusions, join("\t", $gene1, $str1, $exonNumber1, scalar(@exons1), $phase1, "?", "?", "?", "?", "?", "?");
    }
    foreach my $gene2 (keys %{$genes2}) {
      my $str2 = $genes2->{$gene2}{strand};
      $fusion = "Not in Frame";
      $fusion = "In Frame" if $o1 ne $o2 and $str1 eq $str2;
      $fusion = "In Frame" if $o1 eq $o2 and $str1 ne $str2;
      my @exons2 = sort{$genes2->{$gene2}{'exons'}{$a}{'seq_region_start'} <=> $genes2->{$gene2}{'exons'}{$b}{'seq_region_start'} } keys %{$genes2->{$gene2}{'exons'}} if $str2 eq "+";
      @exons2 = sort{$genes2->{$gene2}{'exons'}{$b}{'seq_region_start'} <=> $genes2->{$gene2}{'exons'}{$a}{'seq_region_start'} } keys %{$genes2->{$gene2}{'exons'}} if $str2 eq "-";   

      foreach my $exon (@exons2) {
	my $exonStart = $genes2->{$gene2}{'exons'}{$exon}{'seq_region_start'};
	my $exonEnd = $genes2->{$gene2}{'exons'}{$exon}{'seq_region_end'};
	if ($str2 eq "+") {
	  if ($o2 eq "H") {
	    if ($pos2 >= $exonStart and $pos2 <= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 < $exonStart) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'start_phase'};
	      $exonNumber2 = $rank2;
	      last;
	    }
	  } elsif ($o2 eq "T") {
	    if ($pos2 >= $exonStart and $pos2 <= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 > $exonEnd) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'end_phase'};
	      $exonNumber2 = $rank2;
	    }
	  }
	}
	elsif ($str2 eq "-") {
	  if ($o2 eq "H") {
	    if ($pos2 <= $exonStart and $pos2 >= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 < $exonEnd) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'end_phase'};
	      $exonNumber2 = $rank2;
	    }
	  } elsif ($o2 eq "T") {
	    if ($pos2 <= $exonStart and $pos2 >= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 > $exonStart) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'start_phase'};
	      $exonNumber2 = $rank2;
	      last;
	    }
	  }
	}
	$rank2++;
      }
      $phase = "Not in Phase";
      my $phase1a = $phase1;
      $phase1a = $1 if $phase1 =~ /exonic\((.+)\)/;
      my $phase2a = $phase2;
      $phase2a = $1 if $phase2 =~ /exonic\((.+)\)/;
      
      if ($phase1a == -1) {
	$phase = "In Phase" if $phase1a == $phase2a and $exonNumber1 < scalar(@exons1) and $exonNumber2 < scalar(@exons2);
      } elsif ($phase1a >= 0) {
	$phase = "In Phase" if $phase1a == $phase2a;
      }
      push @fusions, join("\t", $gene1, $str1, $exonNumber1, scalar(@exons1), $phase1, $gene2, $str2, $exonNumber2, scalar(@exons2), $phase2, $fusion, $phase);
    }
  }
  if (scalar(keys %{$genes1}) == 0 and scalar(keys %{$genes2}) > 0) {
    foreach my $gene2 (keys %{$genes2}) {
      my $str2 = $genes2->{$gene2}{strand};
      my @exons2 = sort{$genes2->{$gene2}{'exons'}{$a}{'seq_region_start'} <=> $genes2->{$gene2}{'exons'}{$b}{'seq_region_start'} } keys %{$genes2->{$gene2}{'exons'}} if $str2 eq "+";
      @exons2 = sort{$genes2->{$gene2}{'exons'}{$b}{'seq_region_start'} <=> $genes2->{$gene2}{'exons'}{$a}{'seq_region_start'} } keys %{$genes2->{$gene2}{'exons'}} if $str2 eq "-";   

      foreach my $exon (@exons2) {
	my $exonStart = $genes2->{$gene2}{'exons'}{$exon}{'seq_region_start'};
	my $exonEnd = $genes2->{$gene2}{'exons'}{$exon}{'seq_region_end'};
	if ($str2 eq "+") {
	  if ($o2 eq "H") {
	    if ($pos2 >= $exonStart and $pos2 <= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 < $exonStart) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'start_phase'};
	      $exonNumber2 = $rank2;
	      last;
	    }
	  } elsif ($o2 eq "T") {
	    if ($pos2 >= $exonStart and $pos2 <= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 > $exonEnd) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'end_phase'};
	      $exonNumber2 = $rank2;
	    }
	  }
	}
	elsif ($str2 eq "-") {
	  if ($o2 eq "H") {
	    if ($pos2 <= $exonStart and $pos2 >= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 < $exonEnd) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'end_phase'};
	      $exonNumber2 = $rank2;
	    }
	  } elsif ($o2 eq "T") {
	    if ($pos2 <= $exonStart and $pos2 >= $exonEnd) {
	      $exonNumber2 = $rank2;
	      $phase2 = "exonic";
	      $phase2 .= "(". ($genes2->{$gene2}{'exons'}{$exon}{'start_phase'}+(abs($pos2-$exonStart))) % 3 . ")";
	    } elsif ($pos2 > $exonStart) {
	      $phase2 = $genes2->{$gene2}{'exons'}{$exon}{'start_phase'};
	      $exonNumber2 = $rank2;
	      last;
	    }
	  }
	}
	$rank2++;
      }
      push @fusions, join("\t", "?", "?", "?", "?", "?", $gene2, $str2, $exonNumber2, scalar(@exons2), $phase2, $fusion);
    }
  } elsif (scalar(keys %{$genes1}) == 0 and scalar(keys %{$genes2}) == 0) {
    push @fusions, join("\t", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?");
  }
  return(\@fusions);
}
