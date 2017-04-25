#! /usr/bin/perl

package Sample;

use strict;
use DBI;
use StrucVarDB::RunPlatform;
use StrucVarDB::RunType;
use StrucVarDB::BreakType;
use StrucVarDB::ConfirmType;
use StrucVarDB::Run;
use StrucVarDB::Breakpoint;
use StrucVarDB::Filter;
use StrucVarDB::Stats;
use StrucVarDB::InsertSize;

my $db = "MPDB2";
my $host = "genetics.genomicscenter.nl";
my $user = "MPDB2";
my $pass = "MPDB2";

my $dsn = "DBI:mysql:database=$db;host=$host";
my $dbh = DBI->connect( $dsn, $user, $pass, { RaiseError => 1 }) or die ( "Couldn't connect to database: " . DBI->errstr ); 

sub new {
  my ($class, $id ,$name, $description, $date, $sampleType, $organisation, $group, $category, $species) = @_;
  my %self = (
    'id' => $id,
    'name' => $name,
    'description' => $description,
    'date' => $date,
    'sampleType' => $sampleType,
    'organisation' => $organisation,
    'group' => $group,
    'category' => $category,
    'species' => $species
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

sub date {
  my $self = shift;
  return $self->{'date'};
}

sub sampleType {
  my $self = shift;
  return $self->{'sampleType'};
}

sub organisation {
  my $self = shift;
  return $self->{'organisation'};
}

sub group {
  my $self = shift;
  return $self->{'group'};
}

sub category {
  my $self = shift;
  return $self->{'category'};
}

sub species {
  my $self = shift;
  return $self->{'species'};
}

sub getBreakpoints {
  my $self = shift;
  my $sampleID = $self->id;
  my $query = "SELECT T_breakpoint.*, T_breaktype.breaktype_name, T_confirmType.conType_name, T_confirmType.conType_Description, T_run.run_date, T_run.run_name, T_platforms.platform_ID, T_platforms.platform_name, T_runType.runType_ID, T_runType.runType_name
  FROM T_breakpoint 
  INNER JOIN T_breaktype ON T_breakpoint.T_breaktype_breaktype_ID = T_breaktype.breaktype_ID
  INNER JOIN T_confirmType ON T_breakpoint.T_confirmType_conType_ID = T_confirmType.conType_ID
  INNER JOIN T_run ON T_breakpoint.T_runSamples_T_run_run_ID = T_run.run_ID
  INNER JOIN T_platforms ON T_run.T_platforms_platform_ID = T_platforms.platform_ID
  INNER JOIN T_runType ON T_run.T_runType_runType_ID = T_runType.runType_ID
  WHERE T_runSamples_T_samples_sample_ID = $sampleID";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @breakpoints;
  while (my ($runID, $sampleID, $id, $chr1, $s1, $e1, $mb1, $chr2, $s2, $e2, $mb2, $orientation, $fcount, $rcount, $overlap, $eDistance, $rProbability, $breakTypeID, $confirmTypeID, $breakTypeName, $confirmTypeName, $confirmTypeDescription, $runDate, $runName, $runPlatformID, $runPlatformName, $runTypeID, $runTypeName) = $sth->fetchrow_array()) {
    my $runPlatform = new RunPlatform($runPlatformID, $runPlatformName);
    my $runType = new RunType($runTypeID, $runTypeName);
    my $breakType = new BreakType($breakTypeID, $breakTypeName);
    my $confirmType = new ConfirmType($confirmTypeID, $confirmTypeName, $confirmTypeDescription);
    my $run = new Run($runID, $runDate, $runName, $runPlatform, $runType);
    my $breakpoint = new Breakpoint($id, $run, $self, $chr1, $s1, $e1, $chr2, $s2, $e2, $orientation, $fcount, $rcount, $overlap, $eDistance, $rProbability, $breakType, $confirmType);
    push @breakpoints, $breakpoint;
  }
  return \@breakpoints;

}

sub getRuns {
  my $self = shift;
  my $sampleID = $self->id;
  my $query = "SELECT T_run.*, T_platforms.platform_name, T_runType.runType_name FROM T_run
  INNER JOIN T_runSamples ON T_runSamples.T_run_run_ID = T_run.run_ID 
  INNER JOIN T_platforms ON T_run.T_platforms_platform_ID = T_platforms.platform_ID
  INNER JOIN T_runType ON T_run.T_runType_runType_ID = T_runType.runType_ID
  WHERE T_runSamples.T_samples_sample_ID = $sampleID";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @runs;
  while (my ($runID, $runDate, $runName, $runPlatformID, $runTypeID, $runPlatformName, $runTypeName) = $sth->fetchrow_array()) {
    my $runPlatform = new RunPlatform($runPlatformID, $runPlatformName);
    my $runType = new RunType($runTypeID, $runTypeName);
    my $run = new Run($runID, $runDate, $runName, $runPlatform, $runType);
    push @runs, $run;
  }
  return \@runs;
}

sub getFilters {
  my $self = shift;
  my $sampleID = $self->id;
  my $query = "SELECT DISTINCT * FROM T_filter 
  INNER JOIN T_usedFilters ON T_filter.filterID = T_usedFilters.T_filter_filterID
  INNER JOIN T_filterOptions ON T_usedFilters.T_filterOptions_filterOptionID = T_filterOptions.filterOptionID
  WHERE T_filterOptions.optionType = 'Sample' AND T_filterOptions.optionValue = $sampleID";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @filters;
  while (my ($id, $start, $stop, $progress, $loadedBreaks, $resultBreaks) = $sth->fetchrow_array()) {
    my $filter = new Filter($id, $start, $stop, $progress, $loadedBreaks, $resultBreaks);
    push @filters, $filter;
  }
  return \@filters;
}

sub getStatsByRunID {
  my ($self, $runID) = @_;
  my $sampleID = $self->id;
  my $query = "SELECT * FROM T_stats WHERE T_runSamples_T_samples_sample_ID = $sampleID AND T_runSamples_T_run_run_ID = $runID";
  my $sth = $dbh->prepare($query);
  $sth->execute;
  my @stats;
  while (my ($runID ,$sampleID, $pairsTotal, $pairsNonClonal, $pairsNonClonalPerc, $consistent, $consistentPerc, $consistentNonClonal, $consistentNonClonalPerc, $everted, $evertedPerc, $evertedNonClonal, $evertedNonClonalPerc, $inverted, $invertedPerc, $invertedNonClonal, $invertedNonClonalPerc, $remote, $remotePerc, $remoteNonClonal, $remoteNonClonalPerc) = $sth->fetchrow_array()) {
    my $stats = new Stats($runID ,$sampleID, $pairsTotal, $pairsNonClonal, $pairsNonClonalPerc, $consistent, $consistentPerc, $consistentNonClonal, $consistentNonClonalPerc, $everted, $evertedPerc, $evertedNonClonal, $evertedNonClonalPerc, $inverted, $invertedPerc, $invertedNonClonal, $invertedNonClonalPerc, $remote, $remotePerc, $remoteNonClonal, $remoteNonClonalPerc);
    push @stats, $stats;
  }
  return \@stats;
}

sub getInsertSizesByRunID {
  my ($self, $runID) = @_;
  my $sampleID = $self->id;
  my $query = "SELECT * FROM T_runStats WHERE T_runSamples_T_run_run_ID = $runID AND T_runSamples_T_samples_sample_ID = $sampleID";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @insertSizes;
  while (my ($runID, $sampleID, $size, $count, $perc) = $sth->fetchrow_array()) {
    my $insertSize = new InsertSize($runID, $sampleID, $size, $count, $perc);
    push @insertSizes, $insertSize;
  }
  return \@insertSizes; 
}


1;
