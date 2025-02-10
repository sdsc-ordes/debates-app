<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<div class="info">
		<div class="links">
			<a href="https://github.com/sdsc-ordes/political-debates-ui">
				<i class="fab fa-github"></i>
			</a>
			<a
				href="/edit"
				class="button-primary-dark"
				style="color: var(--on-primary); text-decoration: none; "
				>Edit</a
			>
		</div>
		<h1 style="">UNHCR Political Debates</h1>
		<div>
			Welcome to the Political Debates prototype. This prototype allows you to search and find political debates from the UNHCR
			using keywords in the translations and transcriptions.
			<br />
			Navigate to the search page to start your search. Find debates using
			keywords in the search bar and filter using the facets on the left of
			the screen.
			<br /><br />
			Click on the debate cards to navigate to any debate to find a media player, a list of speakers, and
			full transcript and translation. On this page you can download the text and media files.
			<br /><br />
			If you want to edit the the speaker information or text, go to the edit
			version of this page.
			<br /><br />

			Enjoy!
		</div>

		<div
			class='links'
		>
			<div>
				<a
					href="/search"
					class="button-primary"
					style="color: var(--on-primary); text-decoration: none; background-color: var(--secondary-color);"
				>
					Search
				</a>
			</div>
		</div>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
		/* border-radius: 20px; */
		/* background-color: var(--primary-color); */
	}

	.links {
		display: flex;
		flex-direction: row;
		justify-content: end;
		width: 100%;
		align-items: end;
		gap: 2rem;
		width: 100%;
	}

	.fa-github {
		font-size: 1.5rem;
		color: var(--primary-dark-color);
	}

	a {
		color: var(--secondary-color);
	}

	h1 {
		font-family: var(--body-font);
		font-size: 36px;
		color: var(--primary-dark-color);
		line-height: 1;
		font-weight: bold;
		padding-top: 3rem;
	}

	.info {
		/* background-color: var(--primary-dark-color); */
		border: 2px dashed var(--primary-dark-color);
		padding: 50px;
		color: var(--text-color);
		margin-top: 1rem;
		border-radius: 10px;
		width: 50%;
		justify-content: start;
		align-items: start;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
</style>
