#! /usr/bin/perl

package Species;

use strict;
use StrucVarDB::Sample;
use StrucVarDB::SampleType;
use StrucVarDB::Organisation;
use StrucVarDB::Category;
use StrucVarDB::Group;

my $db = "MPDB2";
my $host = "genetics.genomicscenter.nl";
my $user = "MPDB2";
my $pass = "MPDB2";

my $dsn = "DBI:mysql:database=$db;host=$host";
my $dbh = DBI->connect( $dsn, $user, $pass, { RaiseError => 1 }) or die ( "Couldn't connect to database: " . DBI->errstr ); 

sub new {
  my ($class, $id ,$name, $version) = @_;
  my %self = (
    'id' => $id,
    'name' => $name,
    'version' => $version
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

sub version {
  my $self = shift;
  return $self->{'version'};
}

 sub getSamples {
   my $self = shift;
   my $id = $self->id;
   my $query = "SELECT T_samples.sample_ID, T_samples.sample_name, T_samples.sample_description, T_samples.sample_date, T_sampletype.*, T_organisation.*, T_group.*, T_categoryGroup.*, T_species.* 
   FROM T_samples
   INNER JOIN T_sampletype ON T_samples.T_sampletype_sampletype_ID = T_sampletype.sampletype_ID
   INNER JOIN T_organisation ON T_samples.T_organisation_org_ID = T_organisation.org_ID
   INNER JOIN T_group ON T_samples.T_group_group_ID = T_group.group_ID
   INNER JOIN T_categoryGroup ON T_samples.T_categoryGroup_cat_ID = T_categoryGroup.cat_ID
   INNER JOIN T_species ON T_samples.T_species_species_ID = T_species.species_ID
   WHERE T_species.species_ID = $id";
   my $sth = $dbh->prepare($query);
   $sth->execute();
   my @samples;
   while (my ($sampleID, $sampleName, $sampleDescription, $sampleDate, $sampleTypeID, $sampleTypeName, $organisationID, $organisationName, $groupID, $groupName, $groupDescription, $categoryID, $categoryName, $categoryDescription, $speciesID, $speciesName, $speciesVersion) = $sth->fetchrow_array()) {
     my $sampleType = new SampleType($sampleTypeID, $sampleTypeName);
     my $organisation = new Organisation($organisationID, $organisationName);
     my $group = new Group($groupID, $groupName, $groupDescription);
     my $category = new Category($categoryID, $categoryName, $categoryDescription);
     my $species = $self;
     my $sample = new Sample($sampleID, $sampleName, $sampleDescription, $sampleDate, $sampleType, $organisation,  $group, $category, $species);
     push @samples, $sample;
   }
   return \@samples;  
 }

1;
