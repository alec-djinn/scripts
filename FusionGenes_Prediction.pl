#! /usr/bin/perl

use strict;
use warnings;

# Set libraries:
use lib '/home/amarcozz/src/bioperl-1.2.3';
use lib '/home/amarcozz/src/ensembl/modules';
use lib '/home/amarcozz/src/ensembl-compara/modules';
use lib '/home/amarcozz/src/ensembl-variation/modules';
use lib '/home/amarcozz/src/ensembl-functgenomics/modules';

use Data::Dumper;
use Bio::EnsEMBL::Registry;
use Bio::EnsEMBL::DBSQL::DBAdaptor;

my $reg = "Bio::EnsEMBL::Registry";
   $reg->load_registry_from_db(-host => 'ensembldb.ensembl.org',-user => 'anonymous');
my $sa = $reg->get_adaptor("human", "core", "slice"); 
my $ta = $reg->get_adaptor("human", "core", "transcript" );
my $file = shift;


open F, $file;



my $RoomForPromoter = 100; 
# Use $RoomForPromoter to set at what distance from breakpoint-coordinate to look for genes;
#  (If breakpoint is just before transcription start site, no gene is found while the breakpoint might be in the promoter of that gene).


# Print a header(This will be alligned with all columns in current script):
print "#patientcode\tchr1\tstartcoor1\tendcoor1\tchr2\tstartcoor2\tendcoor2\tori\tBPexact\tDataBase\tVariationType\tInheritance\tfusionName\tfusionID\tfusiontype\tdonorName\tdonorFunction\tdonorBiotype\tdonorStrand\tdonorTranscriptID\tdonorExonID\tdonorExonRank\tdonorExonTotal\tdonorBPinExon\tdonorExonStart\tdonorExonEnd\tdonorExonStartPhase\tdonorBreakpoint\tacceptorName\tacceptorFunction\tacceptorBiotype\tacceptorStrand\tacceptorTranscriptID1\tacceptortExonID\tacceptorExonRank\tacceptorExonTotal\tBPinExon\tacceptorExonStart\tacceptorExonEnd\tacceptorExonStartPhase\tacceptorBreakpoint\tintactORF\tstopCodon\n";



while(<F>) {
chomp;

# Initiate variables:
my ($patientID, $chr1, $start1, $end1, $chr2, $start2, $end2, $ori, $exactBP, $Database, $variationType, $inheritance) = split/\t/, $_;  
   
   
#Select which coordinate is closest to breakpoint:   
my ($pos1, $pos2) = ($start1, $start2);   
 if ($ori =~ /(H|T)(H|T)/i) {      
  $pos1 = $end1 if uc($1) eq "T";      
  $pos2 = $end2 if uc($2) eq "T";       
 }

 
# Attach orientation; Position + orientation is needed to find genes in next step.  
my ($ori1, $ori2);
 if ($ori =~ /(H|T)(H|T)/i) {
  $ori1 = uc($1);
  $ori2 = uc($2);
 }

# actual retrieval of genes from ENSEMBL database.  
my $genes1 = getGenes($chr1, $pos1, $ori1, $RoomForPromoter);
my $genes2 = getGenes($chr2, $pos2, $ori2, $RoomForPromoter);


# Sort all found genes by function: Donors vs. Acceptors.  
my $donors    = getDonors   ($genes1, $genes2);
my $acceptors = getAcceptors($genes1, $genes2);


my $out; 

# Actual mating of every Donor: 
foreach my $donor_gene_id (keys %{$donors}) {
  #look for donors in $genes1 and retrieve info
  if (exists $genes1->{$donor_gene_id}) {
   my $donor_name 				= $genes1->{$donor_gene_id}{'name'};
   my $donor_promVSgene         = $genes1->{$donor_gene_id}{'promVSgene'};
   my $donor_UTRvsCDS;
    foreach my $donor_transcript_id (keys %{$genes1->{$donor_gene_id}{'transcript'}}) {
    $donor_UTRvsCDS             = $genes1->{$donor_gene_id}{'transcript'}{$donor_transcript_id}{'UTRvsCDS'};
    } 
    my $donor_breakpointForStruc = $donor_promVSgene;  
       $donor_breakpointForStruc = $donor_UTRvsCDS if $donor_promVSgene eq 'Gene';  

	  
	  # To each acceptor:
	  foreach my $acceptor_gene_id (keys %{$acceptors}) {      
	    #look in for acceptors in $genes2 and retrieve info(Donor and Accepter have to come from different breakpoint; so only $genes1+$genes2 or $genes2+$genes1)
		if (exists $genes2->{$acceptor_gene_id}) {
		  my $acceptor_name		   = $genes2->{$acceptor_gene_id}{'name'};
		  my $acceptor_promVSgene  = $genes2->{$acceptor_gene_id}{'promVSgene'};
		  my $acceptor_UTRvsCDS;
          foreach my $acceptor_transcript_id (keys %{$genes2->{$acceptor_gene_id}{'transcript'}}) {
            $acceptor_UTRvsCDS           = $genes2->{$acceptor_gene_id}{'transcript'}{$acceptor_transcript_id}{'UTRvsCDS'};
          } 
          my $acceptor_breakpointForStruc = $acceptor_promVSgene;  
	         $acceptor_breakpointForStruc = $acceptor_UTRvsCDS if $acceptor_promVSgene eq 'Gene';
				
				next if $donor_name eq $acceptor_name;
			# If there is a donor and acceptor; info is printed; names, where genes are interrupted, exon info etc.	
		    my $fusionpairID     = $donor_gene_id . "-" . $acceptor_gene_id; 
		    my $fusionpairName   = $donor_name . "-" . $acceptor_name;
		    my $fusionstructure  = $donor_breakpointForStruc . "-" . $acceptor_breakpointForStruc;
         
		     
		    my $info_on_donor;    
		    my $info_on_acceptor; 
		    my $intactORF = "-";
		    my $hybridSTOPcodon = "-";
		 
		    if ($fusionstructure eq 'CDS-CDS'){
		    $info_on_donor       = loopthroughDonor($genes1->{$donor_gene_id});
		    $info_on_acceptor    = loopthroughAcceptor($genes2->{$acceptor_gene_id});
				#this is where framecheck should come in; information on participating exons is available; only frame check to insert.
				#if ($exactBP eq 'yes'){
				#($intactORF, $hybridSTOPcodon) = framecheck($info_on_donor, $info_on_acceptor);
				#}
		    }else{
		    $info_on_donor       = loopthoughGene($genes1->{$donor_gene_id});
		    $info_on_acceptor    = loopthoughGene($genes2->{$acceptor_gene_id});
		 }
		 
			$out .=  $_ . "\t" . $fusionpairName. "\t" . $fusionpairID . "\t" . $fusionstructure . "\t" . join("\t", @{$info_on_donor}[0..12]) . "\t" . join("\t", @{$info_on_acceptor}[0..12]) . "\t" . $intactORF . "\t" . $hybridSTOPcodon . "\n";
        			
	    } 
	 }	
 }
  #look for donors in $genes2 and retrieve info 
  elsif (exists $genes2->{$donor_gene_id}) {
    my $donor_name        = $genes2->{$donor_gene_id}{'name'};
	my $donor_promVSgene = $genes2->{$donor_gene_id}{'promVSgene'};
    my $donor_UTRvsCDS;      
     foreach my $donor_transcript_id (keys %{$genes2->{$donor_gene_id}{'transcript'}}) {
     $donor_UTRvsCDS           = $genes2->{$donor_gene_id}{'transcript'}{$donor_transcript_id}{'UTRvsCDS'};
     } 
	 my $donor_breakpointForStruc = $donor_promVSgene;  
        $donor_breakpointForStruc = $donor_UTRvsCDS if $donor_promVSgene eq 'Gene';  
		
	  # To each acceptor:
	  foreach my $acceptor_gene_id (keys %{$acceptors}) {
        
		#look for acceptors in $genes2 and retrieve info(Donor and Accepter have to come from different breakpoint; so only $genes1+$genes2 or $genes2+$genes1)
		if (exists $genes1->{$acceptor_gene_id}) {
	      my $acceptor_name         = $genes1->{$acceptor_gene_id}{'name'};
		  my $acceptor_promVSgene   = $genes1->{$acceptor_gene_id}{'promVSgene'};
		  my $acceptor_UTRvsCDS;     
          foreach my $acceptor_transcript_id (keys %{$genes1->{$acceptor_gene_id}{'transcript'}}) {
            $acceptor_UTRvsCDS           = $genes1->{$acceptor_gene_id}{'transcript'}{$acceptor_transcript_id}{'UTRvsCDS'};
          } 	
		  my $acceptor_breakpointForStruc = $acceptor_promVSgene;  
             $acceptor_breakpointForStruc = $acceptor_UTRvsCDS if $acceptor_promVSgene eq 'Gene';  

				next if $donor_name eq $acceptor_name;
			# If there is a donor and acceptor; info is printed; names, where genes are interrupted, exon info etc.	 
			my $fusionpairID     = $donor_gene_id . "-" . $acceptor_gene_id; 
		    my $fusionpairName   = $donor_name . "-" . $acceptor_name;
		    my $fusionstructure  = $donor_breakpointForStruc . "-" . $acceptor_breakpointForStruc;
 
		    my $info_on_donor;    
		    my $info_on_acceptor; 
		    my $intactORF = "-";
		    my $hybridSTOPcodon = "-";
		 
		    if ($fusionstructure eq 'CDS-CDS'){
		    $info_on_donor       = loopthroughDonor($genes2->{$donor_gene_id});
		    $info_on_acceptor    = loopthroughAcceptor($genes1->{$acceptor_gene_id});
				#this is where framecheck should come in; information on participating exons is available; only frame check to insert.
				#if ($exactBP eq 'yes'){
				#($intactORF, $hybridSTOPcodon) = framecheck($info_on_donor, $info_on_acceptor);
				#}
		    }else{
		    $info_on_donor       = loopthoughGene($genes2->{$donor_gene_id});
		    $info_on_acceptor    = loopthoughGene($genes1->{$acceptor_gene_id});
		 }

			$out .=  $_ . "\t" . $fusionpairName . "\t" . $fusionpairID . "\t" . $fusionstructure . "\t" . join("\t", @{$info_on_donor}[0..12]) . "\t" . join("\t", @{$info_on_acceptor}[0..12]) . "\t" . $intactORF . "\t" . $hybridSTOPcodon . "\n";

        }
 	  
     }
	 
    } 

}
if (defined $out){ 
print $out
}
}
close F;



#Framecheck;. 
sub framecheck { 
 my ($donor_info, $acceptor_info) = @_;

 # IMPORT of @$donor_info, @$acceptor_info  (works)
 my ($name1, $function1, $biotype1, $strand1, $transcriptID1, $exonID1, $exonRank1, $exonTotal1, $exonic1, $exonStart1, $exonEnd1, $exonStartPhase1, $seq1, $pos1) = @$donor_info;
 my ($name2, $function2, $biotype2, $strand2, $transcriptID2, $exonID2, $exonRank2, $exonTotal2, $exonic2, $exonStart2, $exonEnd2, $exonStartPhase2, $seq2, $pos2) = @$acceptor_info;
	
#print Dumper(@$donor_info);
#print Dumper(@$acceptor_info);
 

# Actual frame-check 

return ($ORF, $stopcodon);
}







# For the Donor: last exon before breakpoint is selected, information into array "@gene_info"
sub loopthroughDonor {
my ($gene) = @_;

my @gene_info;
    
	#initiation of variables:
    my $found = 0;  
    my $trans = "";
    my $exon = "";
    my $seq = "";
    my $str = "";
	
    # For genes on the forward strand:
	if ($gene->{'strand'} == 1){
	  
	  #	For each transcript(Only the canonical transcript currently included)
	  foreach my $transcript_id (keys %{$gene->{'transcript'}}){
		
		# The exons are sorted according to distance from the breakpoint.
		foreach my $exon_id (sort{$gene->{'transcript'}{$transcript_id}{'exons'}{$a}{'dist'} <=> $gene->{'transcript'}{$transcript_id}{'exons'}{$b}{'dist'}} keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}) {
	    
		# Looping until first exon with dist > 0 (First exon with end-coordinate lower than breakpoint coordinate(thus last exon before breakpoint))
		#	or until exon that contains the breakpointcoordinate.
		next unless $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} > 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $found = 1 if $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} > 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $seq = $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'seq'};
	  
	  # Info of selected exon stored in @gene_info:
	  @gene_info = (
	    $gene->{'name'},
		$gene->{'function'},
		$gene->{'biotype'}, 
	    $gene->{'strand'},
		$transcript_id, 
	    $exon_id, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'rank'}, 
	    scalar(keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}), 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'}, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'start'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'end'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'phase'},
	    $gene->{'breakpoint'},
		$seq);
		
	last if $found;
		}
	  }
	}
	  # For genes on the reverse strand:
	  elsif ($gene->{'strand'} == -1){
	  
	  #	For each transcript(Only the canonical transcript currently included)
	  foreach my $transcript_id (keys %{$gene->{'transcript'}}){
		
		# The exons are sorted according to distance from the breakpoint.
		foreach my $exon_id (sort{$gene->{'transcript'}{$transcript_id}{'exons'}{$b}{'dist'} <=> $gene->{'transcript'}{$transcript_id}{'exons'}{$a}{'dist'}} keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}) {
	    
		# Looping until first exon with dist < 0 (First exon with end-coordinate higher than breakpoint coordinate(thus last exon before breakpoint)) 
		# 	or until exon that contains the breakpointcoordinate. 
		next unless $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} < 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $found = 1 if $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} < 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $seq = $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'seq'};
	  
	  # Info of selected exon stored in @gene_info:
	  @gene_info = (
	    $gene->{'name'},
		$gene->{'function'},
		$gene->{'biotype'}, 
	    $gene->{'strand'},
   	    $transcript_id, 
	    $exon_id, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'rank'}, 
	    scalar(keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}), 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'}, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'start'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'end'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'phase'},
	    $gene->{'breakpoint'},
		$seq);		
	last if $found;
        }
	   }
     }
  
  return(\@gene_info);
}



# For the Acceptor: first exon after breakpoint is selected, information into array "@gene_info"
sub loopthroughAcceptor {
my ($gene) = @_;
my @gene_info;
	
	#initiation of variables:
    my $found = 0;  
    my $trans = "";
    my $exon = "";
    my $seq = "";
    my $str = "";
	
	# For genes on the forward strand:
	if ($gene->{'strand'} == 1){
	  
	  #	For each transcript(Only the canonical transcript currently included)
	  foreach my $transcript_id (keys %{$gene->{'transcript'}}){
		
		# The exons are sorted according to distance from the breakpoint. 
		foreach my $exon_id (sort{$gene->{'transcript'}{$transcript_id}{'exons'}{$b}{'dist'} <=> $gene->{'transcript'}{$transcript_id}{'exons'}{$a}{'dist'}} keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}) {
	    
		# Looping until first exon with dist < 0 (First exon with end-coordinate higher than breakpoint coordinate(thus first exon after breakpoint)) 
		#	or until exon that contains the breakpointcoordinate.
		next unless $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} < 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $found = 1 if $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} < 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $seq = $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'seq'};
	  
	  # Info of selected exon stored in @gene_info:
	  @gene_info = (
	    $gene->{'name'},
		$gene->{'function'},
		$gene->{'biotype'}, 
	    $gene->{'strand'},		
   	    $transcript_id, 
	    $exon_id, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'rank'}, 
	    scalar(keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}), 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'}, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'start'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'end'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'phase'},
	    $gene->{'breakpoint'},
		$seq);
	
	last if $found;
		}
	  }
	  }
	  
	# For genes on the reverse strand:
	elsif ($gene->{'strand'} == -1){
	  
	  #	For each transcript(Only the canonical transcript currently included)
	  foreach my $transcript_id (keys %{$gene->{'transcript'}}){
		
		# The exons are sorted according to distance from the breakpoint.
		foreach my $exon_id (sort{$gene->{'transcript'}{$transcript_id}{'exons'}{$a}{'dist'} <=> $gene->{'transcript'}{$transcript_id}{'exons'}{$b}{'dist'}} keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}) {
	    
		# Looping until first exon with dist > 0 (First exon with end-coordinate lower than breakpoint coordinate(thus first exon after breakpoint)) 
		#	or until exon that contains the breakpointcoordinate.
		next unless $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} > 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $found = 1 if $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'dist'} > 0 or $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'} == 1;
	    $seq = $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'seq'};
	  
	  # Info of selected exon stored in @gene_info:
	  @gene_info = (
	    $gene->{'name'},
		$gene->{'function'},
		$gene->{'biotype'}, 
	    $gene->{'strand'},		
   	    $transcript_id, 
	    $exon_id, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'rank'}, 
	    scalar(keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}), 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'exonic'}, 
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'start'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'end'},
	    $gene->{'transcript'}{$transcript_id}{'exons'}{$exon_id}{'phase'},
	    $gene->{'breakpoint'},
		$seq);
	last if $found;
        }
	  }
    }
  
  return(\@gene_info);

}



# If fusion is not CDS-CDS; array initiated with - for empty vallues; matched to Donor and Acceptor; 
#   output rows same length for CDS-CDS and other fusion genes for output file. 
sub loopthoughGene { 
 my ($gene) = @_;
 my @gene_info;
	
 my $exon_id = "-";
 my $exon_rank = "-";
 my $exonic = "-";
 my $exonStart = "-";
 my $exonEnd  = "-";
 my $exonStartPhase = "-"; 
 my $seq = "-";	
		

 foreach my $transcript_id (keys %{$gene->{'transcript'}}){
	
	@gene_info = (
		$gene->{'name'},                                                   #
		$gene->{'function'},                                               # 
		$gene->{'biotype'},                                                #
		$gene->{'strand'},
		$transcript_id,                                                    #
		$exon_id,
		$exon_rank,
		scalar (keys %{$gene->{'transcript'}{$transcript_id}{'exons'}}),   #
		$exonic,
		$exonStart,
		$exonEnd,
		$exonStartPhase,   
		$gene->{'breakpoint'},
		$seq);
		
		
}

 return (\@gene_info);		
		
}





# Actual gene-retrieval from ENSEMBL database. 
#	INPUT:  Coordinates(chromosome, position, orientation, room for promoter) for each contributor of breakpoint
#	OUTPUT: Hash %genes
sub getGenes {  
  my ($chr, $pos, $ori, $prom) = @_;
  my %genes;
  $chr =~ s/^chr//;    
  
  my @genes;
  
  # Make a slice of (breakpoint upto (breakpoint+room for promoter))
  my $slicePlus  = $sa->fetch_by_region('chromosome', $chr, $pos, ($pos+$prom));
  # Get genes on that slice.
  my $genesPlus		 =     $slicePlus->get_all_Genes ; 
  # Only include genes on forward strand. 
  foreach my $gene (@$genesPlus) {
    next if $gene->strand == -1;
	# add to @genes.
	push(@genes, $gene);
 }
  # Make a slice of ((breakpoint-room for promoter) upto breakpoint)
  my $sliceMin = $sa->fetch_by_region('chromosome', $chr, ($pos-$prom), $pos);
  # Get genes on that slice.
  my $genesMin		 =     $sliceMin->get_all_Genes ;  
  # Only include genes on reverse strand.
  foreach my $gene (@$genesMin) {
    next if $gene->strand == 1;
    # add to @genes.
    push(@genes, $gene);
  }
 
  foreach my $gene (@genes) {

    my $strand      = $gene->strand();
    my $biotype     = $gene->biotype();

	# In final output, the strand on which a gene lies is included in the name. 
	my $StrForName 	= "+";
	   $StrForName  = "-" if $strand == -1;
	my $name        = $gene->external_name(). "(" . $StrForName . ")";   
	   
	#  Only protein coding genes are considered
	next unless $biotype eq "protein_coding";
	
	
	#$pos is added to $id because if small dubs or dels 1 gene affected; donor and 
	# acceptor mixed up; by adding pos to id no mix-up possible.
	my $id          = $gene->stable_id() . "(" . $pos . ")"; #(remove $pos here when problem fixed)
	
	# Assign each gene to Donor or Acceptor, according to strand and orientation. 
	my $function    = getFunction($strand, $ori);
	
	# Gene coordinates needed to find where gene is disrupted. 
	my $geneStart   = $gene->seq_region_start();
	my $geneEnd	    = $gene->seq_region_end();

	# Gene is disrupted in promoter region, unless breakpointcoordinate is within gene (between start 5UTR upto end 3UTR)
	my $promVSgene = "Promoter";
	   $promVSgene = "Gene" if ($pos >= $geneStart and $pos <= $geneEnd);
#	(
#   Use this if want to use Ensembl's build-in canonical transcript feature:(     Disable    "my $transcript  = getTranscript($canonical, $pos, $strand, $promVSgene);"    )
#   my $transcript  = $gene->canonical_transcript();   unless $promVSgene eq "Promoter";   ???
#	)	
	
	# If gene disrupted in promoter, no use to find transcripts
	# Used to get all transcripts of the gene.
	my $isoforms    = getIsoforms($gene);                      
	
	# Selects canonical transcript(= longest protein-coding transcript). 
	my $canonical   = getCanonical($isoforms, $pos); 
	
	# Next if gene has no protein-coding transcript. 
	next unless $canonical;							 
	
	#If a canonical transcript is found;
	my $transcript  = getTranscript($canonical, $pos, $strand, $promVSgene);  
	#Attach following information to the transcript:
	$genes{$id}{'name'}        = $name;
	$genes{$id}{'strand'}      = $strand;
    $genes{$id}{'ori'}         = $ori;
	$genes{$id}{'biotype'}     = $biotype;
    $genes{$id}{'function'}    = $function;
    $genes{$id}{'promVSgene'}  = $promVSgene;
	$genes{$id}{'transcript'}  = $transcript;
    $genes{$id}{'breakpoint'}  = $pos;
	
  }
  
  return(\%genes);
}


# After canonical transcript is selected, this sub is used to retreive it, make a hash of it,
#	 and add all relevant information the hash.  
sub getTranscript {
  my ($canonical, $pos, $strand, $promVSgene) = @_;
  my %transcript;
  my $transcript = $ta->fetch_by_stable_id($canonical);
  for my $trans($transcript) {
	my $id       = $trans->display_id();
	my $length   = $trans->length();
	my $biotype  = $trans->biotype();
	
	#transcript WITH UTRs
    my $start    = $trans->seq_region_start();
    my $end      = $trans->seq_region_end();
        
    #transcript WITHOUT UTRs
	my $CDSstart = $trans->coding_region_start();
	my $CDSend   = $trans->coding_region_end();
	
	#calculation of start + end of 5'UTR and 3'UTR
	my $FiveUTRstart  = $start;
	   $FiveUTRstart  = $CDSend +1 if $strand == -1;
	my $FiveUTRend    = $CDSstart -1;
	   $FiveUTRend    = $end if $strand == -1;
	my $ThreeUTRstart = $CDSend +1;
	   $ThreeUTRstart = $start if $strand == -1;
	my $ThreeUTRend   = $end;
	   $ThreeUTRend   = $CDSstart -1 if $strand == -1;

	#See if the breakpoint is in 5UTR, CDS or 3 UTR. (Only if breakpoint is within gene and not in promoter(getGenes --> promVStrans))
	my $UTRvsCDS = 'Promoter';
	if ($promVSgene eq 'Gene'){
       $UTRvsCDS = '5UpStrSeq';
	   $UTRvsCDS = '5UTR' if ($pos >= $FiveUTRstart and $pos <= $FiveUTRend);
	   $UTRvsCDS = 'CDS' if ($pos >= $CDSstart and $pos <= $CDSend);
	   $UTRvsCDS = '3UTR' if ($pos >= $ThreeUTRstart and $pos <= $ThreeUTRend);
	   $UTRvsCDS = '3DownStrSeq' if ($pos >= $ThreeUTRend and $strand == 1);
	   $UTRvsCDS = '3DownStrSeq' if ($pos <= $ThreeUTRstart and $strand == -1);

	}
	
	my $exons = getExons($trans, $pos);
    
	$transcript{$id}{'biotype'}   = $biotype;
	$transcript{$id}{'length'}    = $length;
    $transcript{$id}{'start'}     = $start;
    $transcript{$id}{'end'}       = $end;
	$transcript{$id}{'CDSstart'}  = $CDSstart;
	$transcript{$id}{'CDSend'}    = $CDSend;
	$transcript{$id}{'UTRvsCDS'}  = $UTRvsCDS;
	
	$transcript{$id}{'5UTRstart'} = $FiveUTRstart;
    $transcript{$id}{'5UTRend'}   = $FiveUTRend;
	$transcript{$id}{'3UTRstart'} = $ThreeUTRstart;
	$transcript{$id}{'3UTRend'}   = $ThreeUTRend;
	
	$transcript{$id}{'exons'}     = $exons;
  }  
  return(\%transcript);
}



# This sub retrieves all transcripts of a given gene, returns biotype and length; used to find canonical transcript. 
sub getIsoforms{
	my ($gene) = @_;
	my %isoforms;
	my $isoforms = $gene->get_all_Transcripts();
	foreach my $isoform (@$isoforms) {
      my $id      = $isoform->display_id();
	  my $length  = $isoform->length();
	  my $biotype = $isoform->biotype();
	  my $start   = $isoform->seq_region_start();
	  my $end     = $isoform->seq_region_end();
	  $isoforms{$id}{'length'} = $length;
	  $isoforms{$id}{'biotype'}= $biotype;
	  $isoforms{$id}{'start'}  = $start;
	  $isoforms{$id}{'end'}    = $end;
	 }
	return (\%isoforms);
}


# Canonical transcript is defined as "Longest protein-coding transcript"; found using this sub.  
sub getCanonical{	

	my ($isoforms, $pos) = @_;
	my $canonical;
	my $found = 0;
	
	# Transcripts sorted by length from longest to shortest:
	foreach my $isoform_id (sort {$isoforms->{$b}{'length'} <=> $isoforms->{$a}{'length'}}  keys %{$isoforms}){
	  
	  #looping until: biotype eq "protein_coding"
	  next unless $isoforms->{$isoform_id}{'biotype'} eq "protein_coding";
	  $found = 1 if $isoforms->{$isoform_id}{'biotype'} eq "protein_coding";
	  $canonical = $isoform_id;
	 last if $found;
	}	
	#Returns the id of the canonical transcript:
	return $canonical;
}

#	This sub retrieves all exons of the selected transcript. attaches info. important: dist(distance = pos-exonEnd) 
#	and exonic(exonic = 1 if breakpoint is inside exon)
sub getExons {
  my ($trans, $pos) = @_;
  my $exons = $trans->get_all_Exons();
  my %exons;
  my $rank  = 1;
  foreach my $exon (@$exons) {
    my $id        = $exon->display_id;
    my $exonStart = $exon->seq_region_start();
    my $exonEnd   = $exon->seq_region_end();
    my $seq       = $exon->seq->seq();
    my $phase     = $exon->phase();
    my $dist      = ($pos-$exonEnd); 
    $exons{$id}{'start'}  = $exonStart;
    $exons{$id}{'end'}    = $exonEnd;
	$exons{$id}{'dist'}   = $dist;
    $exons{$id}{'seq'}    = $seq;
    $exons{$id}{'rank'}   = $rank;
    $exons{$id}{'phase'}  = $phase;
    $exons{$id}{'exonic'} = 0;
    $exons{$id}{'exonic'} = 1 if ($pos >= $exonStart and $pos <= $exonEnd);
    $rank++
  }
  return(\%exons);
}

# Function depends on the orientation and the strand of each breakpoint contributor.
sub getFunction{
  my ($strand, $ori) = @_;
  my $function;
  $function = "Donor"    if $ori eq "T" and $strand ==  1;
  $function = "Donor"    if $ori eq "H" and $strand == -1;
  $function = "Acceptor" if $ori eq "T" and $strand == -1;
  $function = "Acceptor" if $ori eq "H" and $strand ==  1;
  return ($function);
}




# Find all Donors within all found genes
sub getDonors{
  my ($genes1, $genes2) = @_;
  my %donors;
  
  # For every gene found on the first breakpointcoordinate:
  foreach my $gene_id1 (keys %{$genes1}) {
    
	#Add to %donors if the gene function (sub getFunction;--> $genes{$id}{'function'}) = "Donor"
	my $function = $genes1->{$gene_id1}{'function'};
    $donors{$gene_id1} = 1 if $function eq "Donor";
  }
  
  # For every gene found on the second breakpointcoordinate:
  foreach my $gene_id2 (keys %{$genes2}) {
    
	#Add to %donors if the gene function (sub getFunction;--> $genes{$id}{'function'}) = "Donor"
	my $function = $genes2->{$gene_id2}{'function'};
    $donors{$gene_id2} = 1 if $function eq "Donor";
  }
return (\%donors);
}



# Find all Acceptors within all found genes
sub getAcceptors{
  my ($genes1, $genes2) = @_;
  my %acceptors;
  
  # For every gene found on the first breakpointcoordinate:
  foreach my $gene_id1 (keys %{$genes1}) {
    
	#Add to %acceptors if the gene function (sub getFunction;--> $genes{$id}{'function'}) = "Acceptor"
	my $function = $genes1->{$gene_id1}{'function'};
    $acceptors{$gene_id1} = 1 if $function eq "Acceptor";
  }
  # For every gene found on the second breakpointcoordinate:
  foreach my $gene_id2 (keys %{$genes2}) {
    
	#Add to %acceptors if the gene function (sub getFunction;--> $genes{$id}{'function'}) = "Acceptor"
	my $function = $genes2->{$gene_id2}{'function'};
    $acceptors{$gene_id2} = 1 if $function eq "Acceptor";
  }
return (\%acceptors);
}
	