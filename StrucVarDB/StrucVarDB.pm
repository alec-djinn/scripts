# ! /usr/bin/perl

package StrucVarDB; 

use strict;
use DBI;
use StrucVarDB::SampleType;
use StrucVarDB::Organisation;
use StrucVarDB::Group;
use StrucVarDB::Category;
use StrucVarDB::Species;
use StrucVarDB::Sample;
use StrucVarDB::Filter;
use Data::Dumper;

my $db = "MPDB2";
my $host = "genetics.genomicscenter.nl";
my $user = "MPDB2";
my $pass = "MPDB2";

my $dsn = "DBI:mysql:database=$db;host=$host";
my $dbh = DBI->connect( $dsn, $user, $pass, { RaiseError => 1 }) or die ( "Couldn't connect to database: " . DBI->errstr ); 

sub new {
  my ($class) = @_;
  my %self = ();
  return bless \%self, $class;
}

sub getAllSamples {
  my $self = shift;
  my $query = "SELECT T_samples.sample_ID, T_samples.sample_name, T_samples.sample_description, T_samples.sample_date, T_sampletype.*, T_organisation.*, T_group.*, T_categoryGroup.*, T_species.* 
  FROM T_samples
  INNER JOIN T_sampletype ON T_samples.T_sampletype_sampletype_ID = T_sampletype.sampletype_ID
  INNER JOIN T_organisation ON T_samples.T_organisation_org_ID = T_organisation.org_ID
  INNER JOIN T_group ON T_samples.T_group_group_ID = T_group.group_ID
  INNER JOIN T_categoryGroup ON T_samples.T_categoryGroup_cat_ID = T_categoryGroup.cat_ID
  INNER JOIN T_species ON T_samples.T_species_species_ID = T_species.species_ID";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @samples;
  while (my ($sampleID, $sampleName, $sampleDescription, $sampleDate, $sampleTypeID, $sampleTypeName, $organisationID, $organisationName, $groupID, $groupName, $groupDescription, $categoryID, $categoryName, $categoryDescription, $speciesID, $speciesName, $speciesVersion) = $sth->fetchrow_array()) {
    my $sampleType = new SampleType($sampleTypeID, $sampleTypeName);
    my $organisation = new Organisation($organisationID, $organisationName);
    my $group = new Group($groupID, $groupName, $groupDescription);
    my $category = new Category($categoryID, $categoryName, $categoryDescription);
    my $species = new Species($speciesID, $speciesName, $speciesVersion);
    my $sample = new Sample($sampleID, $sampleName, $sampleDescription, $sampleDate, $sampleType, $organisation,  $group, $category, $species);
    push @samples, $sample;
  }
  return \@samples;
}

sub getAllFilters {
  my $self = shift;
  my $query = "SELECT * FROM T_filter";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @filters;
  while (my ($id, $start, $stop, $progress, $loaded, $breakpoints) = $sth->fetchrow_array) {
    my $filter = new Filter($id, $start, $stop, $progress, $loaded, $breakpoints);
    push @filters, $filter;
  }
  return \@filters;
}

sub getAllGroups{
  my $query = "SELECT * FROM T_group";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @groups;
  while (my ($id, $name, $description) = $sth->fetchrow_array()) {
    my $group = new Group($id, $name, $description);
    push @groups, $group;
  }
  return \@groups;
}

sub getAllSampleTypes {
  my $query = "SELECT * FROM T_sampletype";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @sampleTypes;
  while (my ($id, $name) = $sth->fetchrow_array()) {
    my $sampleType = new SampleType($id, $name);
    push @sampleTypes, $sampleType;
  }
  return \@sampleTypes;
}

sub getAllOrganisations {
  my $query = "SELECT * FROM T_organisation";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @organisations;
  while (my ($id, $name) = $sth->fetchrow_array()) {
    my $organisation = new Organisation($id, $name);
    push @organisations, $organisation;
  }
  return \@organisations;
}

sub getAllSpecies {
  my $query = "SELECT * FROM T_species";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @species;
  while (my ($id, $name, $version) = $sth->fetchrow_array()) {
    my $species = new Species($id, $name, $version);
    push @species, $species;
  }
  return \@species;
}

sub getAllCategories {
  my $query = "SELECT * FROM T_categoryGroup";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @catergories;
  while (my ($id, $name, $description) = $sth->fetchrow_array()) {
    my $catergory = new Category($id, $name, $description);
    push @catergories, $catergory;
  }
  return \@catergories;
}

sub getAllRuns {
  my $query = "SELECT T_run.*, T_platforms.platform_name, T_runType.runType_name FROM T_run
  INNER JOIN T_platforms ON T_run.T_platforms_platform_ID = T_platforms.platform_ID
  INNER JOIN T_runType ON T_run.T_runType_runType_ID = T_runType.runType_ID";
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

sub getAllBreakTypes {
  my $query = "SELECT * FROM T_breaktype";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @breakTypes;
  while (my ($id, $name) = $sth->fetchrow_array()) {
    my $breakType = new BreakType($id, $name);
    push @breakTypes, $breakType;
  }
  return \@breakTypes;
}

sub getAllConfirmTypes {
  my $query = "SELECT * FROM T_confirmType";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @confirmTypes;
  while (my ($id, $name, $description) = $sth->fetchrow_array()) {
    my $confirmType = new ConfirmType($id, $name, $description);
    push @confirmTypes, $confirmType;
  }
  return \@confirmTypes;
}

sub getAllRunPlatforms {
  my $query = "SELECT * FROM T_platforms";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @runPlatforms;
  while (my ($id, $name) = $sth->fetchrow_array()) {
    my $runPlatform = new RunPlatform($id, $name);
    push @runPlatforms, $runPlatform;
  }
  return \@runPlatforms;
}

sub getAllRunTypes {
  my $query = "SELECT * FROM T_runType";
  my $sth = $dbh->prepare($query);
  $sth->execute();
  my @runTypes;
  while (my ($id, $name) = $sth->fetchrow_array()) {
    my $runType = new RunType($id, $name);
    push @runTypes, $runType;
  }
  return \@runTypes;
}

sub searchBreakpoints {
	my ($self, @options) = @_;
	my ($c1, $s1, $e1, $c2, $s2, $e2, $orientation, $type);
	foreach my $option (@options) {
		if ($option =~ /^[TH]{2}$/) {
			$orientation = $option;
		} elsif ($option =~ /^(\w{1,2})(:(\d+)-(\d+))?$/) {
			($c2, $s2, $e2) = ($1, $3, $4) if $c1;
			($c1, $s1, $e1) = ($1, $3, $4) unless $c1;
		} elsif ($option =~ /^[a-z]+$/) {
			$type = $option;
		} else {
			die "Unknown option:\t$option\n";
		}
	}
	my $whereQuery = " WHERE ";
	if ($s1 and $s2) {
		$whereQuery .= "((T_breakpoint.break_chr1 = '$c1' AND T_breakpoint.break_chr1_start <= $e1 AND T_breakpoint.break_chr1_end >= $s1)
		AND (T_breakpoint.break_chr2 = '$c2' AND T_breakpoint.break_chr2_start <= $e2 AND T_breakpoint.break_chr2_end >= $s2))
		OR ((T_breakpoint.break_chr2 = '$c1' AND T_breakpoint.break_chr2_start <= $e1 AND T_breakpoint.break_chr2_end >= $s1)
		AND (T_breakpoint.break_chr1 = '$c2' AND T_breakpoint.break_chr1_start <= $e2 AND T_breakpoint.break_chr1_end >= $s2))";
	} elsif ($s1 and !$s2 and $c2) {
		$whereQuery .= "((T_breakpoint.break_chr1 = '$c1' AND T_breakpoint.break_chr1_start <= $e1 AND T_breakpoint.break_chr1_end >= $s1)
		AND (T_breakpoint.break_chr2 = '$c2'))
		OR ((T_breakpoint.break_chr2 = '$c1' AND T_breakpoint.break_chr2_start <= $e1 AND T_breakpoint.break_chr2_end >= $s1)
		AND (T_breakpoint.break_chr1 = '$c2'))";
	} elsif ($s1 and !$c2) {
		$whereQuery .= "((T_breakpoint.break_chr1 = '$c1' AND T_breakpoint.break_chr1_start <= $e1 AND T_breakpoint.break_chr1_end >= $s1)
		OR ((T_breakpoint.break_chr2 = '$c1' AND T_breakpoint.break_chr2_start <= $e1 AND T_breakpoint.break_chr2_end >= $s1))";
	} elsif (!$s1 and $c1 and $s2) {
		$whereQuery .= "((T_breakpoint.break_chr1 = '$c1')
		AND (T_breakpoint.break_chr2 = '$c2' AND T_breakpoint.break_chr2_start <= $e2 AND T_breakpoint.break_chr2_end >= $s2))
		OR ((T_breakpoint.break_chr2 = '$c1')
		AND (T_breakpoint.break_chr1 = '$c2' AND T_breakpoint.break_chr1_start <= $e2 AND T_breakpoint.break_chr1_end >= $s2))";
	} elsif (!$s1 and $c1 and !$s2 and $c2) {
		$whereQuery .= "((T_breakpoint.break_chr1 = '$c1')
		AND (T_breakpoint.break_chr2 = '$c2'))
		OR ((T_breakpoint.break_chr2 = '$c1')
		AND (T_breakpoint.break_chr1 = '$c2'))";
	} elsif (!$s1 and $c1 and !$s2 and !$c2) {
		print "chr-X\n";
		$whereQuery .= "((T_breakpoint.break_chr1 = '$c1')
		OR ((T_breakpoint.break_chr2 = '$c1'))";
	} else {
		die "No region(s) or chromosome(s) found!\n";
	}
	my $query = "SELECT T_breakpoint.*, T_breaktype.breaktype_name, T_confirmType.conType_name, T_confirmType.conType_Description, T_run.run_date, T_run.run_name, T_platforms.platform_ID, T_platforms.platform_name, T_runType.runType_ID, T_runType.runType_name,
	T_samples.sample_ID, T_samples.sample_name, T_samples.sample_description, T_samples.sample_date, T_sampletype.*, T_organisation.*, T_group.*, T_categoryGroup.*, T_species.* 
	FROM T_breakpoint 
	INNER JOIN T_breaktype ON T_breakpoint.T_breaktype_breaktype_ID = T_breaktype.breaktype_ID
	INNER JOIN T_confirmType ON T_breakpoint.T_confirmType_conType_ID = T_confirmType.conType_ID
	INNER JOIN T_run ON T_breakpoint.T_runSamples_T_run_run_ID = T_run.run_ID
	INNER JOIN T_platforms ON T_run.T_platforms_platform_ID = T_platforms.platform_ID
	INNER JOIN T_runType ON T_run.T_runType_runType_ID = T_runType.runType_ID
	INNER JOIN T_samples ON T_samples.sample_ID = T_breakpoint.T_runSamples_T_samples_sample_ID
	INNER JOIN T_sampletype ON T_samples.T_sampletype_sampletype_ID = T_sampletype.sampletype_ID
	INNER JOIN T_organisation ON T_samples.T_organisation_org_ID = T_organisation.org_ID
	INNER JOIN T_group ON T_samples.T_group_group_ID = T_group.group_ID
	INNER JOIN T_categoryGroup ON T_samples.T_categoryGroup_cat_ID = T_categoryGroup.cat_ID
	INNER JOIN T_species ON T_samples.T_species_species_ID = T_species.species_ID";
	$query .= $whereQuery;
	my $sth = $dbh->prepare($query);
	$sth->execute();
	my @breakpoints;
	while (my ($runID, $sampleID, $id, $chr1, $s1, $e1, $mb1, $chr2, $s2, $e2, $mb2, $orientation, $fcount, $rcount, $overlap, $eDistance, $rProbability, $breakTypeID, $confirmTypeID, $breakTypeName, $confirmTypeName, $confirmTypeDescription, $runDate, $runName, $runPlatformID, $runPlatformName, $runTypeID, $runTypeName, $sampleID, $sampleName, $sampleDescription, $sampleDate, $sampleTypeID, $sampleTypeName, $organisationID, $organisationName, $groupID, $groupName, $groupDescription, $categoryID, $categoryName, $categoryDescription, $speciesID, $speciesName, $speciesVersion) = $sth->fetchrow_array()) {
		my $runPlatform = new RunPlatform($runPlatformID, $runPlatformName);
		my $runType = new RunType($runTypeID, $runTypeName);
		my $breakType = new BreakType($breakTypeID, $breakTypeName);
		my $confirmType = new ConfirmType($confirmTypeID, $confirmTypeName, $confirmTypeDescription);
		my $run = new Run($runID, $runDate, $runName, $runPlatform, $runType);
		my $sampleType = new SampleType($sampleTypeID, $sampleTypeName);
		my $organisation = new Organisation($organisationID, $organisationName);
		my $group = new Group($groupID, $groupName, $groupDescription);
		my $category = new Category($categoryID, $categoryName, $categoryDescription);
		my $species = new Species($speciesID, $speciesName, $speciesVersion);
		my $sample = new Sample($sampleID, $sampleName, $sampleDescription, $sampleDate, $sampleType, $organisation,  $group, $category, $species);
		my $breakpoint = new Breakpoint($id, $run, $sample, $chr1, $s1, $e1, $chr2, $s2, $e2, $orientation, $fcount, $rcount, $overlap, $eDistance, $rProbability, $breakType, $confirmType);
		push @breakpoints, $breakpoint;
	}
	return \@breakpoints;
}
1;
