#!/usr/bin/perl

my $pid=12488; #insert here monitored process PID

#returns current process time counters or single undef if unavailable
#returns:  1. process counter  , 2. system counter , 3. total system cpu cores
sub GetCurrentLoads {
    my $pid=shift;
    my $fh;
    my $line;
    open $fh,'<',"/proc/$pid/stat" or return undef;
    $line=<$fh>;
    close $fh;
    return undef unless $line=~/^\d+ \([^)]+\) \S \d+ \d+ \d+ \d+ -?\d+ \d+ \d+ \d+ \d+ \d+ (\d+) (\d+)/;
    my $TimeApp=$1+$2;
    my $TimeSystem=0;
    my $CpuCount=0;
    open $fh,'<',"/proc/stat" or return undef;
    while (defined($line=<$fh>)) {
        if ($line=~/^cpu\s/) {
            foreach my $nr ($line=~/\d+/g) { $TimeSystem+=$nr; };
            next;
        };
        $CpuCount++ if $line=~/^cpu\d/;
    }
    close $fh;
    return undef if $TimeSystem==0;
    return $TimeApp,$TimeSystem,$CpuCount;
}

my ($currApp,$currSys,$lastApp,$lastSys,$cores);
while () {
    ($currApp,$currSys,$cores)=GetCurrentLoads($pid);
    printf "Load is: %5.1f\%\n",($currApp-$lastApp)/($currSys-$lastSys)*$cores*100 if defined $currApp and defined $lastApp and defined $currSys and defined $lastSys;
    ($lastApp,$lastSys)=($currApp,$currSys);
    sleep 1;
}
