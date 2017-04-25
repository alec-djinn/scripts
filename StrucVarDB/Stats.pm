#! /usr/bin/perl

package Stats; 

use strict;

sub new {
  my ($class, $runID ,$sampleID, $pairsTotal, $pairsNonClonal, $pairsNonClonalPerc, $consistent, $consistentPerc, $consistentNonClonal, $consistentNonClonalPerc, $everted, $evertedPerc, $evertedNonClonal, $evertedNonClonalPerc, $inverted, $invertedPerc, $invertedNonClonal, $invertedNonClonalPerc, $remote, $remotePerc, $remoteNonClonal, $remoteNonClonalPerc) = @_;
  my %self = (
    'runID' => $runID,
    'sampleID' => $sampleID,
    'pairsTotal' => $pairsTotal,
    'pairsNonClonal' => $pairsNonClonal,
    'pairsNonClonalPerc' => $pairsNonClonalPerc,
    'consistent' => $consistent,
    'consistentPerc' => $consistentPerc,
    'consistentNonClonal' => $consistentNonClonal,
    'consistentNonClonalPerc' => $consistentNonClonalPerc,
    'everted' => $everted,
    'evertedPerc' => $evertedPerc,
    'evertedNonClonal' => $evertedNonClonal,
    'evertedNonClonalPerc' => $evertedNonClonalPerc,
    'inverted' => $inverted,
    'invertedPerc' => $invertedPerc,
    'invertedNonClonal' => $invertedNonClonal,
    'invertedNonClonalPerc' => $invertedNonClonalPerc,
    'remote' => $remote,
    'remotePerc' => $remotePerc,
    'remoteNonClonal' => $remoteNonClonal,
    'remoteNonClonalPerc' => $remoteNonClonalPerc
  );
  return bless \%self, $class;
}

sub runID {
  my $self = shift;
  return $self->{'runID'};
}

sub sampleID {
  my $self = shift;
  return $self->{'sampleID'};
}

sub pairsTotal {
  my $self = shift;
  return $self->{'pairsTotal'};
}

sub pairsNonClonal {
  my $self = shift;
  return $self->{'pairsNonClonal'};
}

sub pairsNonClonalPerc {
  my $self = shift;
  return $self->{'pairsNonClonalPerc'};
}

sub consistent {
  my $self = shift;
  return $self->{'consistent'};
}

sub consistentPerc {
  my $self = shift;
  return $self->{'consistentPerc'};
}

sub consistentNonClonal {
  my $self = shift;
  return $self->{'consistentNonClonal'};
}

sub consistentNonClonalPerc {
  my $self = shift;
  return $self->{'consistentNonClonalPerc'};
}

sub everted {
  my $self = shift;
  return $self->{'everted'};
}

sub evertedPerc {
  my $self = shift;
  return $self->{'evertedPerc'};
}

sub evertedNonClonal {
  my $self = shift;
  return $self->{'evertedNonClonal'};
}

sub evertedNonClonalPerc {
  my $self = shift;
  return $self->{'evertedNonClonalPerc'};
}

sub inverted {
  my $self = shift;
  return $self->{'inverted'};
}

sub invertedPerc {
  my $self = shift;
  return $self->{'invertedPerc'};
}

sub invertedNonClonal {
  my $self = shift;
  return $self->{'invertedNonClonal'};
}

sub invertedNonClonalPerc {
  my $self = shift;
  return $self->{'invertedNonClonalPerc'};
}

sub remote {
  my $self = shift;
  return $self->{'remote'};
}

sub remotePerc {
  my $self = shift;
  return $self->{'remotePerc'};
}

sub remoteNonClonal {
  my $self = shift;
  return $self->{'remoteNonClonal'};
}

sub remoteNonClonalPerc {
  my $self = shift;
  return $self->{'remoteNonClonalPerc'};
}

1;
