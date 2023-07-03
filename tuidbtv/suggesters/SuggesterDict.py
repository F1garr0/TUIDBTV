from textual.suggester import Suggester, SuggestFromList


class SuggesterDict(SuggestFromList):

    async def get_suggestion(self, value: str) -> str | None:
        if not value.endswith(' '):
            values = value.rsplit(' ', 1)
            last_word = values[-1]
            for idx, suggestion in enumerate(self._for_comparison):
                if suggestion.startswith(last_word):
                    values[-1] = self._suggestions[idx]
                    return ' '.join(values)
        return None
