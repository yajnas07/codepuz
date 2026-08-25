SCENES_QL = sort find count transform copyif boolpred minmax reverse \
           unique removeif fill generate replaceif partition issorted \
           binarysearch nthelement withstrings projections viewspipeline

TITLES_QL = tc-sort tc-find tc-count tc-transform tc-copyif tc-boolpred \
            tc-minmax tc-reverse tc-unique tc-removeif tc-fill tc-generate \
            tc-replaceif tc-partition tc-issorted tc-binarysearch \
            tc-nthelement tc-withstrings tc-projections tc-viewspipeline

SCENES_QH = $(SCENES_QL:%=%-hd)
TITLES_QH = $(TITLES_QL:%=%-hd)

.PHONY: all all-hd titles titles-hd clean $(SCENES_QL) $(SCENES_QH) $(TITLES_QL) $(TITLES_QH)

all: $(SCENES_QL)
all-hd: $(SCENES_QH)
titles: $(TITLES_QL)
titles-hd: $(TITLES_QH)

intro:           ; manim render -ql ranges-algo0.py RangesIntro
intro-hd:        ; manim render -qh ranges-algo0.py RangesIntro

sort:            ; manim render -ql ranges-algo1.py RangesSort
find:            ; manim render -ql ranges-algo1.py RangesFind
count:           ; manim render -ql ranges-algo1.py RangesCount
transform:       ; manim render -ql ranges-algo1.py RangesTransform
copyif:          ; manim render -ql ranges-algo2.py RangesCopyIf
boolpred:        ; manim render -ql ranges-algo2.py RangesBoolPredicates
minmax:          ; manim render -ql ranges-algo3.py RangesMinMax
reverse:         ; manim render -ql ranges-algo3.py RangesReverse
unique:          ; manim render -ql ranges-algo4.py RangesUnique
removeif:        ; manim render -ql ranges-algo4.py RangesRemoveIf
fill:            ; manim render -ql ranges-algo5.py RangesFill
generate:        ; manim render -ql ranges-algo5.py RangesGenerate
replaceif:       ; manim render -ql ranges-algo6.py RangesReplaceIf
partition:       ; manim render -ql ranges-algo6.py RangesPartition
issorted:        ; manim render -ql ranges-algo7.py RangesIsSorted
binarysearch:    ; manim render -ql ranges-algo7.py RangesBinarySearch
nthelement:      ; manim render -ql ranges-algo8.py RangesNthElement
withstrings:     ; manim render -ql ranges-algo8.py RangesWithStrings
projections:     ; manim render -ql ranges-algo9.py RangesProjections
viewspipeline:   ; manim render -ql ranges-algo10.py RangesViewsPipeline

sort-hd:         ; manim render -qh ranges-algo1.py RangesSort
find-hd:         ; manim render -qh ranges-algo1.py RangesFind
count-hd:        ; manim render -qh ranges-algo1.py RangesCount
transform-hd:    ; manim render -qh ranges-algo1.py RangesTransform
copyif-hd:       ; manim render -qh ranges-algo2.py RangesCopyIf
boolpred-hd:     ; manim render -qh ranges-algo2.py RangesBoolPredicates
minmax-hd:       ; manim render -qh ranges-algo3.py RangesMinMax
reverse-hd:      ; manim render -qh ranges-algo3.py RangesReverse
unique-hd:       ; manim render -qh ranges-algo4.py RangesUnique
removeif-hd:     ; manim render -qh ranges-algo4.py RangesRemoveIf
fill-hd:         ; manim render -qh ranges-algo5.py RangesFill
generate-hd:     ; manim render -qh ranges-algo5.py RangesGenerate
replaceif-hd:    ; manim render -qh ranges-algo6.py RangesReplaceIf
partition-hd:    ; manim render -qh ranges-algo6.py RangesPartition
issorted-hd:     ; manim render -qh ranges-algo7.py RangesIsSorted
binarysearch-hd: ; manim render -qh ranges-algo7.py RangesBinarySearch
nthelement-hd:   ; manim render -qh ranges-algo8.py RangesNthElement
withstrings-hd:  ; manim render -qh ranges-algo8.py RangesWithStrings
projections-hd:  ; manim render -qh ranges-algo9.py RangesProjections
viewspipeline-hd:; manim render -qh ranges-algo10.py RangesViewsPipeline

# ---- title card targets (low quality) ----
tc-sort:          ; manim render -ql title_cards.py TitleSort
tc-find:          ; manim render -ql title_cards.py TitleFind
tc-count:         ; manim render -ql title_cards.py TitleCount
tc-transform:     ; manim render -ql title_cards.py TitleTransform
tc-copyif:        ; manim render -ql title_cards.py TitleCopyIf
tc-boolpred:      ; manim render -ql title_cards.py TitleBoolPred
tc-minmax:        ; manim render -ql title_cards.py TitleMinMax
tc-reverse:       ; manim render -ql title_cards.py TitleReverse
tc-unique:        ; manim render -ql title_cards.py TitleUnique
tc-removeif:      ; manim render -ql title_cards.py TitleRemoveIf
tc-fill:          ; manim render -ql title_cards.py TitleFill
tc-generate:      ; manim render -ql title_cards.py TitleGenerate
tc-replaceif:     ; manim render -ql title_cards.py TitleReplaceIf
tc-partition:     ; manim render -ql title_cards.py TitlePartition
tc-issorted:      ; manim render -ql title_cards.py TitleIsSorted
tc-binarysearch:  ; manim render -ql title_cards.py TitleBinarySearch
tc-nthelement:    ; manim render -ql title_cards.py TitleNthElement
tc-withstrings:   ; manim render -ql title_cards.py TitleWithStrings
tc-projections:   ; manim render -ql title_cards.py TitleProjections
tc-viewspipeline: ; manim render -ql title_cards.py TitleViewsPipeline

# ---- title card targets (HD) ----
tc-sort-hd:          ; manim render -qh title_cards.py TitleSort
tc-find-hd:          ; manim render -qh title_cards.py TitleFind
tc-count-hd:         ; manim render -qh title_cards.py TitleCount
tc-transform-hd:     ; manim render -qh title_cards.py TitleTransform
tc-copyif-hd:        ; manim render -qh title_cards.py TitleCopyIf
tc-boolpred-hd:      ; manim render -qh title_cards.py TitleBoolPred
tc-minmax-hd:        ; manim render -qh title_cards.py TitleMinMax
tc-reverse-hd:       ; manim render -qh title_cards.py TitleReverse
tc-unique-hd:        ; manim render -qh title_cards.py TitleUnique
tc-removeif-hd:      ; manim render -qh title_cards.py TitleRemoveIf
tc-fill-hd:          ; manim render -qh title_cards.py TitleFill
tc-generate-hd:      ; manim render -qh title_cards.py TitleGenerate
tc-replaceif-hd:     ; manim render -qh title_cards.py TitleReplaceIf
tc-partition-hd:     ; manim render -qh title_cards.py TitlePartition
tc-issorted-hd:      ; manim render -qh title_cards.py TitleIsSorted
tc-binarysearch-hd:  ; manim render -qh title_cards.py TitleBinarySearch
tc-nthelement-hd:    ; manim render -qh title_cards.py TitleNthElement
tc-withstrings-hd:   ; manim render -qh title_cards.py TitleWithStrings
tc-projections-hd:   ; manim render -qh title_cards.py TitleProjections
tc-viewspipeline-hd: ; manim render -qh title_cards.py TitleViewsPipeline

SC0 = media/videos/ranges-algo0/480p15
TC = media/videos/title_cards/480p15
SC1 = media/videos/ranges-algo1/480p15
SC2 = media/videos/ranges-algo2/480p15
SC3 = media/videos/ranges-algo3/480p15
SC4 = media/videos/ranges-algo4/480p15
SC5 = media/videos/ranges-algo5/480p15
SC6 = media/videos/ranges-algo6/480p15
SC7 = media/videos/ranges-algo7/480p15
SC8 = media/videos/ranges-algo8/480p15
SC9 = media/videos/ranges-algo9/480p15
SC10 = media/videos/ranges-algo10/480p15

MERGE_ORDER = \
	$(SC0)/RangesIntro.mp4 \
	$(TC)/TitleSort.mp4 \
	$(SC1)/RangesSort.mp4 \
	$(TC)/TitleFind.mp4 \
	$(SC1)/RangesFind.mp4 \
	$(TC)/TitleCount.mp4 \
	$(SC1)/RangesCount.mp4 \
	$(TC)/TitleTransform.mp4 \
	$(SC1)/RangesTransform.mp4 \
	$(TC)/TitleCopyIf.mp4 \
	$(SC2)/RangesCopyIf.mp4 \
	$(TC)/TitleBoolPred.mp4 \
	$(SC2)/RangesBoolPredicates.mp4 \
	$(TC)/TitleMinMax.mp4 \
	$(SC3)/RangesMinMax.mp4 \
	$(TC)/TitleReverse.mp4 \
	$(SC3)/RangesReverse.mp4 \
	$(TC)/TitleUnique.mp4 \
	$(SC4)/RangesUnique.mp4 \
	$(TC)/TitleRemoveIf.mp4 \
	$(SC4)/RangesRemoveIf.mp4 \
	$(TC)/TitleFill.mp4 \
	$(SC5)/RangesFill.mp4 \
	$(TC)/TitleGenerate.mp4 \
	$(SC5)/RangesGenerate.mp4 \
	$(TC)/TitleReplaceIf.mp4 \
	$(SC6)/RangesReplaceIf.mp4 \
	$(TC)/TitlePartition.mp4 \
	$(SC6)/RangesPartition.mp4 \
	$(TC)/TitleIsSorted.mp4 \
	$(SC7)/RangesIsSorted.mp4 \
	$(TC)/TitleBinarySearch.mp4 \
	$(SC7)/RangesBinarySearch.mp4 \
	$(TC)/TitleNthElement.mp4 \
	$(SC8)/RangesNthElement.mp4 \
	$(TC)/TitleWithStrings.mp4 \
	$(SC8)/RangesWithStrings.mp4 \
	$(TC)/TitleProjections.mp4 \
	$(SC9)/RangesProjections.mp4 \
	$(TC)/TitleViewsPipeline.mp4 \
	$(SC10)/RangesViewsPipeline.mp4

MERGE_ORDER_HD = $(subst /480p15/,/1080p60/,$(MERGE_ORDER))

define NEWLINE


endef

# List of title card mp4s (480p) that need a silent audio track added
TC_FILES_480 = $(filter $(TC)/%,$(MERGE_ORDER))
TC_FILES_HD  = $(filter $(subst 480p15,1080p60,$(TC))/%,$(MERGE_ORDER_HD))

# Add silent audio to a title card mp4 in-place
define add_silence
	ffmpeg -y -i $(1) -f lavfi -i anullsrc=r=48000:cl=stereo -c:v copy -c:a aac -shortest $(1).tmp.mp4
	mv $(1).tmp.mp4 $(1)
endef

.PHONY: merge merge-hd intro intro-hd

merge:
	@echo "Adding silent audio to title cards..."
	$(foreach f,$(TC_FILES_480),$(call add_silence,$(f))$(NEWLINE))
	$(file >concat_480.txt,$(subst $(NEWLINE) file,$(NEWLINE)file,$(foreach f,$(MERGE_ORDER),$(NEWLINE)file '$(f)')))
	ffmpeg -y -f concat -safe 0 -i concat_480.txt -c copy media/CppRanges_480p.mp4
	@rm -f concat_480.txt
	@echo "Merged: media/CppRanges_480p.mp4"

merge-hd:
	@echo "Adding silent audio to title cards..."
	$(foreach f,$(TC_FILES_HD),$(call add_silence,$(f))$(NEWLINE))
	$(file >concat_1080.txt,$(subst $(NEWLINE) file,$(NEWLINE)file,$(foreach f,$(MERGE_ORDER_HD),$(NEWLINE)file '$(f)')))
	ffmpeg -y -f concat -safe 0 -i concat_1080.txt -c copy media/CppRanges_1080p.mp4
	@rm -f concat_1080.txt
	@echo "Merged: media/CppRanges_1080p.mp4"

clean:
	rm -rf media
