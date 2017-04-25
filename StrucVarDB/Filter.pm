#! /usr/bin/perl

package Filter;

use strict;
use DBI;
use StrucVarDB::FilterOption;
use StrucVarDB::RunPlatform;
use StrucVarDB::RunType;
use StrucVarDB::BreakType;
use StrucVarDB::ConfirmType;
use StrucVarDB::Run;
use StrucVarDB::SampleType;
use StrucVarDB::Organisation;
use StrucVarDB::Group;
use StrucVarDB::Category;
use StrucVarDB::Species;
use StrucVarDB::Sample;
use StrucVarDB::Breakpoint;
use StrucVarDB::FilterResult;

my $db = "MPDB2";
my $host = "genetics.genomicscenter.nl";
my $user = "MPDB2";
my $pass = "MPDB2";

my $dsn = "DBI:mysql:database=$db;host=$host";
my $dbh = DBI->connect( $dsn, $user, $pass, { RaiseError => 1 }) or die ( "Couldn't connect to database: " . DBI->errstr ); 

sub new {
  my ($class, $id, $start, $stop, $progress, $loadedBreaks, $resultBreaks) = @_;
  my %self = (
    'id' => $id,
    'start' => $start,
    'stop' => $stop,
    'progress' => $progress,
    'loadedBreaks' => $loadedBreaks,
    'resultBreaks' => $resultBreaks
  );
  return bless \%self, $class;
}

sub id {
  my $self = shift;
  return $self->{'id'};
}

sub start {
  my $self = shift;
  return $self->{'start'};
}

sub stop {
  my $self = shift;
  return $self->{'stop'};
}

sub progress {
  my $self = shift;
  return $self->{'progress'};
}

sub loadedBreaks {
  my $self = shift;
  return $self->{'loadedBreaks'};
}

sub resultBreaks {
  my $self = shift;
  return $self->{'resultBreaks'};
}

sub getOptions {
  my $self = shift;
  my $filterID = $self->id;
  my $query = "SELECT T_filterOptions.* FROM  T_filterOptions 
    INNER JOIN T_usedFilters ON T_usedFilters.T_filterOptions_filterOptionID = T_filterOptions.filterOptionID 
    WHERE T_usedFilters.T_filter_filterID = $filterID";
  my $sth = $dbh->prepare($query);
  $sth->execute;
  my @filterOptions;
  while (my ($id, $optionType, $optionValue, $optionAction, $option_breakCount, $option_breakOverlap, $option_breakEdistance, $option_break_rprobability) = $sth->fetchrow_array()) {
    my $filterOption = new FilterOption($id, $optionType, $optionValue, $optionAction, $option_breakCount, $option_breakOverlap, $option_breakEdistance, $option_break_rprobability);
    push @filterOptions, $filterOption;
  }
  return \@filterOptions;

}

sub getResults {
  my $self = shift;
  my $id = $self->id;
  my $query = "SELECT T_results.numberSamples, T_breakpoint.*, T_breaktype.breaktype_name, T_confirmType.conType_name, T_confirmType.conType_Description, T_run.run_date, T_run.run_name, T_platforms.platform_ID, T_platforms.platform_name, T_runType.runType_ID, T_runType.runType_name,
  sample_ID, sample_name, sample_description, sample_date, T_sampletype.*, T_organisation.*,  T_group.*, T_categoryGroup.*, T_species.*
  FROM T_breakpoint 
  INNER JOIN T_breaktype ON T_breakpoint.T_breaktype_breaktype_ID = T_breaktype.breaktype_ID
  INNER JOIN T_confirmType ON T_breakpoint.T_confirmType_conType_ID = T_confirmType.conType_ID
  INNER JOIN T_run ON T_breakpoint.T_runSamples_T_run_run_ID = T_run.run_ID
  INNER JOIN T_platforms ON T_run.T_platforms_platform_ID = T_platforms.platform_ID
  INNER JOIN T_runType ON T_run.T_runType_runType_ID = T_runType.runType_ID
  INNER JOIN T_results ON T_results.T_breakpoint_break_ID = T_breakpoint.break_ID
  INNER JOIN T_samples ON T_breakpoint.T_runSamples_T_samples_sample_ID = T_samples.sample_ID
  INNER JOIN T_sampletype ON T_samples.T_sampletype_sampletype_ID = T_sampletype.sampletype_ID
  INNER JOIN T_organisation ON T_samples.T_organisation_org_ID = T_organisation.org_ID
  INNER JOIN T_group ON T_samples.T_group_group_ID = T_group.group_ID
  INNER JOIN T_species ON T_samples.T_species_species_ID = T_species.species_ID
  INNER JOIN T_categoryGroup ON T_samples.T_categoryGroup_cat_ID = T_categoryGroup.cat_ID
  WHERE T_results.T_filter_filterID = $id";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @filterResults;
  while (my ($numberSamples, $runID, $sampleID, $breakID, $chr1, $s1, $e1, $mb1, $chr2, $s2, $e2, $mb2, $orientation, $fcount, $rcount, $overlap, $eDistance, $rProbability, $breakTypeID, $confirmTypeID, $breakTypeName, $confirmTypeName, $confirmTypeDescription, $runDate, $runName, $runPlatformID, $runPlatformName, $runTypeID, $runTypeName, $sampleID, $sampleName, $sampleDescription, $sampleDate, $sampletypeID, $sampletypeName, $organisationID, $organisationName, $groupID, $groupName, $groupDescription, $categoryID, $categoryName, $categoryDescription, $speciesID, $speciesName, $speciesVersion) = $sth->fetchrow_array()) {
    my $runPlatform = new RunPlatform($runPlatformID, $runPlatformName);
    my $runType = new RunType($runTypeID, $runTypeName);
    my $breakType = new BreakType($breakTypeID, $breakTypeName);
    my $confirmType = new ConfirmType($confirmTypeID, $confirmTypeName, $confirmTypeDescription);
    my $run = new Run($runID, $runDate, $runName, $runPlatform, $runType);
    my $sampleType = new SampleType($sampletypeID, $sampletypeName);
    my $organisation = new Organisation($organisationID, $organisationName);
    my $group = new Group($groupID, $groupName, $groupDescription);
    my $category = new Category($categoryID, $categoryName, $categoryDescription);
    my $species = new Species($speciesID, $speciesName, $speciesVersion);
    my $sample = new Sample($sampleID, $sampleName, $sampleDescription, $sampleDate, $sampleType, $organisation,  $group, $category, $species);
    my $breakpoint = new Breakpoint($breakID, $run, $sample, $chr1, $s1, $e1, $chr2, $s2, $e2, $orientation, $fcount, $rcount, $overlap, $eDistance, $rProbability, $breakType, $confirmType);
    my $filterResult = new FilterResult($breakpoint, $self, $numberSamples);
    push @filterResults, $filterResult;
  }
  return \@filterResults;
}

1;