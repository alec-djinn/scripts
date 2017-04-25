#! /usr/bin/perl

package Breakpoint;

use strict;

sub new {
  my ($class, $id, $run, $sample, $chr1, $s1, $e1, $chr2, $s2, $e2, $orientation, $fcount, $rcount, $overlap, $eDistance, $rProbability, $breakType, $confirmType) = @_;
  my %self = (
    'id' => $id,
    'run' => $run,
    'sample' => $sample,
    'chr1' => $chr1,
    's1' => $s1,
    'e1' => $e1,
    'chr2' => $chr2,
    's2' => $s2,
    'e2' => $e2,
    'orientation' => $orientation,
    'Fcount' => $fcount,
    'Rcount' => $rcount,
    'overlap' => $overlap,
    'eDistance' => $eDistance,
    'rProbability' => $rProbability,
    'breakType' => $breakType,
    'confirmType' => $confirmType
  );
  return bless \%self, $class;
}

sub id {
  my $self = shift;
  return $self->{'id'};
}

sub run {
  my $self = shift;
  return $self->{'run'};
}

sub sample {
  my $self = shift;
  return $self->{'sample'};
}

sub chr1 {
  my $self = shift;
  return $self->{'chr1'};
}

sub s1 {
  my $self = shift;
  return $self->{'s1'};
}

sub e1 {
  my $self = shift;
  return $self->{'e1'};
}

sub chr2 {
  my $self = shift;
  return $self->{'chr2'};
}

sub s2 {
  my $self = shift;
  return $self->{'s2'};
}

sub e2 {
  my $self = shift;
  return $self->{'e2'};
}

sub orientation {
  my $self = shift;
  return $self->{'orientation'};
}

sub Fcount {
  my $self = shift;
  return $self->{'Fcount'};
}

sub Rcount {
  my $self = shift;
  return $self->{'Rcount'};
}

sub overlap {
  my $self = shift;
  return $self->{'overlap'};
}

sub eDistance {
  my $self = shift;
  return $self->{'eDistance'};
}

sub rProbability {
  my $self = shift;
  return $self->{'rProbability'};
}

sub breakType {
  my $self = shift;
  return $self->{'breakType'};
}

sub confirmType {
  my $self = shift;
  return $self->{'confirmType'};
}

sub count {
  my $self = shift;
  my $count = $self->{'Fcount'} + $self->{'Rcount'};
  return $count;
}

1;
