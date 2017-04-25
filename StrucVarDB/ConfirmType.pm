#! /usr/bin/perl

package ConfirmType;

use strict;

sub new {
  my ($class, $id ,$name, $description) = @_;
  my %self = (
    'id' => $id,
    'name' => $name,
    'description' => $description
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

sub description {
  my $self = shift;
  return $self->{'description'};
}

1;
