#! /usr/bin/perl

package InsertSize;

use strict;

sub new {
  my ($class, $runID, $sampleID, $insertSize, $insertCount, $insertPerc) = @_;
  my %self = (
    'runID' => $runID,
    'sampleID' => $sampleID,
    'insertSize' => $insertSize,
    'insertCount' => $insertCount,
    'insertPerc' => $insertPerc
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

sub insertSize {
  my $self = shift;
  return $self->{'insertSize'};
}

sub insertCount {
  my $self = shift;
  return $self->{'insertCount'};
}

sub insertPerc {
  my $self = shift;
  return $self->{'insertPerc'};
}

1;
