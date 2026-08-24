SCENES_QL = sort find count transform copyif boolpred minmax reverse \
           unique removeif fill generate replaceif partition issorted \
           binarysearch nthelement withstrings projections viewspipeline

SCENES_QH = $(SCENES_QL:%=%-hd)

.PHONY: all all-hd clean $(SCENES_QL) $(SCENES_QH)

all: $(SCENES_QL)
all-hd: $(SCENES_QH)

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

MERGE_ORDER = \
	media/videos/ranges-algo1/480p15/RangesSort.mp4 \
	media/videos/ranges-algo1/480p15/RangesFind.mp4 \
	media/videos/ranges-algo1/480p15/RangesCount.mp4 \
	media/videos/ranges-algo1/480p15/RangesTransform.mp4 \
	media/videos/ranges-algo2/480p15/RangesCopyIf.mp4 \
	media/videos/ranges-algo2/480p15/RangesBoolPredicates.mp4 \
	media/videos/ranges-algo3/480p15/RangesMinMax.mp4 \
	media/videos/ranges-algo3/480p15/RangesReverse.mp4 \
	media/videos/ranges-algo4/480p15/RangesUnique.mp4 \
	media/videos/ranges-algo4/480p15/RangesRemoveIf.mp4 \
	media/videos/ranges-algo5/480p15/RangesFill.mp4 \
	media/videos/ranges-algo5/480p15/RangesGenerate.mp4 \
	media/videos/ranges-algo6/480p15/RangesReplaceIf.mp4 \
	media/videos/ranges-algo6/480p15/RangesPartition.mp4 \
	media/videos/ranges-algo7/480p15/RangesIsSorted.mp4 \
	media/videos/ranges-algo7/480p15/RangesBinarySearch.mp4 \
	media/videos/ranges-algo8/480p15/RangesNthElement.mp4 \
	media/videos/ranges-algo8/480p15/RangesWithStrings.mp4 \
	media/videos/ranges-algo9/480p15/RangesProjections.mp4 \
	media/videos/ranges-algo10/480p15/RangesViewsPipeline.mp4

MERGE_ORDER_HD = $(subst /480p15/,/1080p60/,$(MERGE_ORDER))

define NEWLINE


endef

.PHONY: merge merge-hd

merge:
	$(file >concat_480.txt,$(subst $(NEWLINE) file,$(NEWLINE)file,$(foreach f,$(MERGE_ORDER),$(NEWLINE)file '$(f)')))
	ffmpeg -y -f concat -safe 0 -i concat_480.txt -c copy media/CppRanges_480p.mp4
	@rm -f concat_480.txt
	@echo "Merged: media/CppRanges_480p.mp4"

merge-hd:
	$(file >concat_1080.txt,$(subst $(NEWLINE) file,$(NEWLINE)file,$(foreach f,$(MERGE_ORDER_HD),$(NEWLINE)file '$(f)')))
	ffmpeg -y -f concat -safe 0 -i concat_1080.txt -c copy media/CppRanges_1080p.mp4
	@rm -f concat_1080.txt
	@echo "Merged: media/CppRanges_1080p.mp4"

clean:
	rm -rf media
