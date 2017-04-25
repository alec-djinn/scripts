#! /usr/bin/perl

package FilterOption;

use strict;

sub new {
  my ($class, $id, $type ,$value, $action, $count, $overlap, $eDistance, $rProbability) = @_;
  my %self = (
    'id' => $id,
    'type' => $type,
    'value' => $value,
    'action' => $action,
    'count' => $count,
    'overlap' => $overlap,
    'eDistance' => $eDistance,
    'rProbability' => $rProbability
  );
  return bless \%self, $class;
}

sub id {
  my $self = shift;
  return $self->{'id'};
}

sub type{
  my $self = shift;
  return $self->{'type'};
}

sub value {
  my $self = shift;
  return $self->{'value'};
}

sub action {
  my $self = shift;
  return $self->{'action'};
}

sub count {
  my $self = shift;
  return $self->{'count'};
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

1;
