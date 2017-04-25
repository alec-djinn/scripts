#! /usr/bin/perl

package RunPlatform;

use strict;

sub new {
  my ($class, $id ,$name) = @_;
  my %self = (
    'id' => $id,
    'name' => $name
  );
  return bless \%self, $class;
}

sub id {
  my $self = shift;
  return $self->{'id'};
}

sub name {
  my $self = shift;
  return $self->{'name'};
}

1;
