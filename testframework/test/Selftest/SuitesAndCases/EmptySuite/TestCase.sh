#--variantCount=4
#--TTRO_casePrep:=copyAndModifyTestCollection
#--TTRO_caseStep:=getOptions runRunTTF myEvaluate

declare -a options=( '' '-j 1' '-j 1 -v' '-j 1 -v -d' )

function getOptions {
	TT_runOptions="${options[$TTRO_caseVariant]}"
}

function myEvaluate {
	linewisePatternMatch './STDERROUT1.log' 'true' '*\*\*\*\*\* case variants=0 skipped=0 failures=0 errors=0' '*\*\*\*\*\* suite variants=1'
}