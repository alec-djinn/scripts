#! /usr/bin/perl

package FilterResult;

use strict;

sub new {
  my ($class, $breakpoint, $filter, $samples) = @_;
  my %self = (
    'breakpoint' => $breakpoint,
    'filter' => $filter,
    'samples' => $samples
  );
  return bless \%self, $class;
}

sub breakpoint {
  my $self = shift;
  return $self->{'breakpoint'};
}

sub filter {
  my $self = shift;
  return $self->{'filter'};
}

sub samples {
  my $self = shift;
  return $self->{'samples'};
}

1;
